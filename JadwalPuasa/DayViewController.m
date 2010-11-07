//
//  DayViewController.m
//  JadwalPuasa
//
//  Created by Dody Suria Wijaya on 7/31/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "DayViewController.h"
#import "PrayerTimeJs.h"

@implementation DayViewController
@synthesize label, startFasting, stopFasting, currentDate, dayForDate;
/*
 // The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
    }
    return self;
}
*/

- (id)initWithDate:(NSDate*)date {
    if (self = [super initWithNibName:@"DayViewController" bundle:nil]) {
        dayForDate = date;
    }
    return self;
}

- (void)viewDidLoad {
	[super viewDidLoad];
	int timezone = 7;
	float latitude = -6.255846;
	float longitude = 106.789615;
	NSArray* time = [[PrayerTimeJs shared] calcPrayerTimeWithDate:dayForDate Latitude:latitude Longitude:longitude TimeZone:timezone];
	if ([time count] > 0) {
		startFasting.text = [time objectAtIndex:0];
		stopFasting.text = [time objectAtIndex:5];
		NSDateFormatter *format = [[NSDateFormatter alloc] init];
		[format setDateFormat:@"dd MMMM yyyy"];
		currentDate.text = [format stringFromDate:dayForDate];
	}
}

/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

- (void)didReceiveMemoryWarning {
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

- (void)viewDidUnload {
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}


- (void)dealloc {
	[label release];
	[startFasting release];
	[stopFasting release];
	[currentDate release];
	[dayForDate release];
    [super dealloc];
}


@end
