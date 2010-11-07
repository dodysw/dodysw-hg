//
//  PrayerTimeJs.h
//  JadwalPuasa
//
//  Created by Dody Suria Wijaya on 7/28/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface PrayerTimeJs : NSObject {
	UIWebView* web;
}
@property (nonatomic, retain) UIWebView* web;
+ (PrayerTimeJs*) shared;
- (NSArray*) calcPrayerTimeWithDate: (NSDate*) date Latitude: (float) latitude Longitude: (float) longitude TimeZone: (int) timezone;
@end
