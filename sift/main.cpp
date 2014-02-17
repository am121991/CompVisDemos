#include <stdio.h>
#include <iostream>
#include <algorithm>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/nonfree/nonfree.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace cv;

void readme();

/** @function main */
int main( int argc, char** argv )
{
  //
  Mat img_object;
  if (argc > 1){
	  printf("img: %s\n", argv[1]);
	  img_object = imread(argv[1]);
  }
  else {
	  printf("default img\n");
	  img_object = imread( "card2.png" );
  }
  if( !img_object.data) { std::cout << " --(!) Error reading image " << std::endl; return -1; }
  
  VideoCapture cap(0);
  if(!cap.isOpened()) { std::cout << " --(!) Error reading video " << std::endl; return -1; }
  
  namedWindow("output",1);
  Mat img_scene;
  
  std::vector<KeyPoint> keypoints_object, keypoints_scene;
  Mat descriptors_object, descriptors_scene;
  
  SiftFeatureDetector detector;
  SiftDescriptorExtractor extractor;

  //-- Step 1: Detect the keypoints using SURF Detector
  detector.detect( img_object, keypoints_object );
  //-- Step 2: Calculate descriptors (feature vectors)
  extractor.compute( img_object, keypoints_object, descriptors_object );
  
  int key1, key2 = false;

  for(;;) {
    cap >> img_scene;
    
    //-- Step 1: Detect the keypoints using SURF Detector
    detector.detect( img_scene, keypoints_scene );
    //-- Step 2: Calculate descriptors (feature vectors)
    extractor.compute( img_scene, keypoints_scene, descriptors_scene );
    
    //-- Step 3: Matching descriptor vectors using FLANN matcher
    FlannBasedMatcher matcher;
    std::vector< DMatch > matches;
    matcher.match( descriptors_object, descriptors_scene, matches );
    
    double max_dist = 0; double min_dist = 100;
    
    //-- Quick calculation of max and min distances between keypoints
    for( int i = 0; i < descriptors_object.rows; i++ )
    { double dist = matches[i].distance;
      if( dist < min_dist ) min_dist = dist;
      if( dist > max_dist ) max_dist = dist;
    }
    
    printf("max | min: %f | %f\n", max_dist, min_dist );
    
    //-- Draw top 50 matches
    std::vector< DMatch > good_matches;
    std::sort(matches.begin(), matches.end());
    for( int i = 0; i < min(descriptors_object.rows, 50); i++ ){
      good_matches.push_back( matches[i]);
    }
    
    Mat img_matches, img_matches2;
    int match_flag = (key2 ? DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS : DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
    if(key1){
      drawMatches( img_object, keypoints_object, img_scene, keypoints_scene,
                good_matches, img_matches, Scalar::all(-1), Scalar::all(-1),
                vector<char>(), match_flag );
      
      //-- Localize the object
      std::vector<Point2f> obj;
      std::vector<Point2f> scene;
      
      for( int i = 0; i < good_matches.size(); i++ )
      {
        //-- Get the keypoints from the good matches
        obj.push_back( keypoints_object[ good_matches[i].queryIdx ].pt );
        scene.push_back( keypoints_scene[ good_matches[i].trainIdx ].pt );
      }
      
      try {
        Mat H = findHomography( obj, scene, CV_RANSAC );
        
        //-- Get the corners from the image_1 ( the object to be "detected" )
        std::vector<Point2f> obj_corners(4);
        obj_corners[0] = cvPoint(0,0); obj_corners[1] = cvPoint( img_object.cols, 0 );
        obj_corners[2] = cvPoint( img_object.cols, img_object.rows ); obj_corners[3] = cvPoint( 0, img_object.rows );
        std::vector<Point2f> scene_corners(4);
        
        perspectiveTransform( obj_corners, scene_corners, H);
        
        //-- Draw lines between the corners (the mapped object in the scene - image_2 )
        line( img_matches, scene_corners[0] + Point2f( img_object.cols, 0), scene_corners[1] + Point2f( img_object.cols, 0), Scalar(0, 255, 0), 4 );
        line( img_matches, scene_corners[1] + Point2f( img_object.cols, 0), scene_corners[2] + Point2f( img_object.cols, 0), Scalar( 0, 255, 0), 4 );
        line( img_matches, scene_corners[2] + Point2f( img_object.cols, 0), scene_corners[3] + Point2f( img_object.cols, 0), Scalar( 0, 255, 0), 4 );
        line( img_matches, scene_corners[3] + Point2f( img_object.cols, 0), scene_corners[0] + Point2f( img_object.cols, 0), Scalar( 0, 255, 0), 4 );
      } catch (...) {
        std::cout << "--(!) Homography error, no worries bro" << std::endl;
      }
      
      //-- Show detected matches
      imshow("output", img_matches );
    }else{
      drawKeypoints(img_object, keypoints_object, img_matches, Scalar(255, 0, 255), match_flag);
      drawKeypoints(img_scene, keypoints_scene, img_matches2, Scalar::all(-1), match_flag);
      
      imshow("output", img_matches );
      imshow("output2", img_matches2 );
    }
    
    //cout << waitKey(30) << endl;
    switch(waitKey(30)){
      case -1:
        break;
      case 49:
        key1 = !key1;
        break;
      case 50:
        key2 = !key2;
        break;
      case 27:
      default:
        return 0;
    }
  }
  return 0;
}
