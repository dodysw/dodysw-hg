//
//  DayViewController.h
//  JadwalPuasa
//
//  Created by Milda Irhamni on 7/31/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface DayViewController : UIViewController {
	IBOutlet UILabel* label;
	IBOutlet UILabel* startFasting;
	IBOutlet UILabel* stopFasting;
	IBOutlet UILabel* currentDate;
	NSDate* dayForDate;
}
@property (nonatomic, retain) IBOutlet UILabel* label;
@property (nonatomic, retain) IBOutlet UILabel* startFasting;
@property (nonatomic, retain) IBOutlet UILabel* stopFasting;
@property (nonatomic, retain) IBOutlet UILabel* currentDate;
@property (nonatomic, retain) NSDate* dayForDate;
- (id)initWithDate:(NSDate*)date;
@end
