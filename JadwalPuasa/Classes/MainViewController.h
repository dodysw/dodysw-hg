//
//  MainViewController.h
//  JadwalPuasa
//
//  Created by Dody Suria Wijaya on 7/28/10.
//  Copyright __MyCompanyName__ 2010. All rights reserved.
//

#import "FlipsideViewController.h"

@interface MainViewController : UIViewController <UIScrollViewDelegate, FlipsideViewControllerDelegate> {
	IBOutlet UIScrollView* scroller;
	NSMutableArray* viewControllers;
	NSDate* launchDate;
}
@property (nonatomic, retain) IBOutlet UIScrollView* scroller;
@property (nonatomic, retain) NSMutableArray* viewControllers;
@property (nonatomic, retain) NSDate* launchDate;

- (IBAction)showInfo:(id)sender;
- (void) loadScrollViewWithPage:(int)page;
@end
