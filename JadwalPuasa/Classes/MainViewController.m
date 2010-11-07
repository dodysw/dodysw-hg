//
//  MainViewController.m
//  JadwalPuasa
//
//  Created by Dody Suria Wijaya on 7/28/10.
//  Copyright __MyCompanyName__ 2010. All rights reserved.
//

#import "MainViewController.h"
#import "DayViewController.h"

@implementation MainViewController
@synthesize scroller, viewControllers, launchDate;

// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
	[super viewDidLoad];
	
	scroller.pagingEnabled = YES;
	scroller.contentSize = CGSizeMake(scroller.frame.size.width * 3, scroller.frame.size.height);
	scroller.showsVerticalScrollIndicator = NO;
	scroller.showsHorizontalScrollIndicator = NO;
	scroller.scrollsToTop = NO;
	
	launchDate = [[NSDate alloc] init];
	
	NSMutableArray *controllers = [[NSMutableArray alloc] init];
    for (unsigned i = 0; i < 3; i++) {
        [controllers addObject:[NSNull null]];
    }
    self.viewControllers = controllers;
    [controllers release];
	
	[self loadScrollViewWithPage:0];
    [self loadScrollViewWithPage:1];
	
}

- (void) scrollViewDidScroll:(UIScrollView*) sender {
	
}

- (void) loadScrollViewWithPage:(int)page {
	if (page < 0) {
		return;
	}
	
	DayViewController* controller = [viewControllers objectAtIndex:page];
	if ((NSNull* ) controller == [NSNull null]) {
		controller = [[DayViewController alloc] initWithDate:[NSDate dateWithTimeInterval:3600*24*page sinceDate:launchDate]];
		[viewControllers replaceObjectAtIndex:page withObject:controller];
		[controller release];
	}
	
	if (controller.view.superview == nil) {
		CGRect frame = scroller.frame;
		frame.origin.x = frame.size.width * page;
		frame.origin.y = 0;
		controller.view.frame = frame;
		[scroller addSubview:controller.view];
	}
	
}

- (void)flipsideViewControllerDidFinish:(FlipsideViewController *)controller {
	[self dismissModalViewControllerAnimated:YES];
}


- (IBAction)showInfo:(id)sender {    
	FlipsideViewController *controller = [[FlipsideViewController alloc] initWithNibName:@"FlipsideView" bundle:nil];
	controller.delegate = self;
	controller.modalTransitionStyle = UIModalTransitionStyleFlipHorizontal;
	[self presentModalViewController:controller animated:YES];
	[controller release];
}


- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
	// Release any cached data, images, etc. that aren't in use.
}


- (void)viewDidUnload {
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}


/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
	// Return YES for supported orientations.
	return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/


- (void)dealloc {
	[viewControllers release];
	[scroller release];
	[launchDate release];
    [super dealloc];
}


@end
