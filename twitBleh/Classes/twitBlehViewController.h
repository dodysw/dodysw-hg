//
//  twitBlehViewController.h
//  twitBleh
//
//  Created by Dody Suria Wijaya on 4/27/10.
//  Copyright __MyCompanyName__ 2010. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface twitBlehViewController : UIViewController <UIPickerViewDelegate, UIPickerViewDataSource>
{
	IBOutlet UIButton *tweetItButton;
	IBOutlet UIPickerView *picker;
	IBOutlet UITextField *note;
	NSArray *feelData;
	NSArray *doData;
}
@property (retain, nonatomic) UIButton *tweetItButton;
@property (retain, nonatomic) UIPickerView *picker;
@property (retain, nonatomic) UITextField *note;

@property (retain, nonatomic) NSArray *feelData;
@property (retain, nonatomic) NSArray *doData;

-(IBAction) tweetItPressed:(id)sender;
-(IBAction) doneWritingNote:(id)sender;

@end

