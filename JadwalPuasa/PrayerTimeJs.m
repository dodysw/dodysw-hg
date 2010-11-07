//
//  PrayerTimeJs.m
//  JadwalPuasa
//
//  Created by Dody Suria Wijaya on 7/28/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "PrayerTimeJs.h"


@implementation PrayerTimeJs
@synthesize web;

static PrayerTimeJs* sharedObject = nil;

+ (PrayerTimeJs*) shared {
	if (!sharedObject) {
		sharedObject = [[[self alloc] init] autorelease];
	}
	return sharedObject;
}

- (id) init {
	self = [super init];
	web = [[UIWebView alloc] init];
	NSString* path = [[NSBundle mainBundle] pathForResource:@"prayTime" ofType:@"js"];
	NSString* js = [NSString stringWithContentsOfFile:path encoding:NSUTF8StringEncoding error:nil];
	[web stringByEvaluatingJavaScriptFromString:js];
	return self;
}

- (NSArray*) calcPrayerTimeWithDate: (NSDate*) date Latitude: (float) latitude Longitude: (float) longitude TimeZone: (int) timezone {
	NSString* result;
	NSDateFormatter *formatter = [[NSDateFormatter alloc] init];
	[formatter setDateFormat:@"yyyy,MM,dd"];
	NSString* mymethod = [NSString stringWithFormat:@"var times = prayTime.getPrayerTimes(new Date(%@), %f, %f, %d); times.join('|');", [formatter stringFromDate: date], latitude, longitude, timezone];
	[formatter release];
	NSLog(@"Method:%@", mymethod);
	result = [web stringByEvaluatingJavaScriptFromString: mymethod];	
	NSLog(@"Result:%@", result);
	return [result componentsSeparatedByString:@"|"];
}

- (void) dealloc {
	[web release];
	sharedObject = nil;
	[super dealloc];
}

@end
