//
//  twitBlehViewController.m
//  twitBleh
//
//  Created by Dody Suria Wijaya on 4/27/10.
//  Copyright __MyCompanyName__ 2010. All rights reserved.
//

#import "twitBlehViewController.h"

@implementation twitBlehViewController
@synthesize picker, tweetItButton, feelData, doData, note;

-(IBAction) doneWritingNote:(id)sender
{
	[note resignFirstResponder];
}

-(IBAction) tweetItPressed:(id)sender
{
	NSString *doWhat = [doData objectAtIndex:[picker selectedRowInComponent:0]];
	NSString *feelWhat = [feelData objectAtIndex:[picker selectedRowInComponent:1]];
	NSString *theMessage = [NSString stringWithFormat:@"I'm %@, and feeling %@ at the moment. %@", doWhat, feelWhat, note.text];
	//NSLog(theMessage);
	NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL: [NSURL URLWithString:@"http://gudangberas:XXXXX@twitter.com/statuses/update.xml"] 
							cachePolicy:NSURLRequestUseProtocolCachePolicy 
						timeoutInterval:60.0];
	[request setHTTPMethod:@"POST"];
	[request setHTTPBody:[[NSString stringWithFormat:@"status=%@", theMessage] dataUsingEncoding:NSASCIIStringEncoding]];

	NSURLResponse *response;
	NSError *error;
	NSData *data = [NSURLConnection sendSynchronousRequest:request 
										 returningResponse:&response 
													 error:&error];
	NSLog(@"Returned: %@", [[NSString alloc] initWithData:data encoding:NSASCIIStringEncoding]);
	
	
}

-(NSInteger) numberOfComponentsInPickerView:(UIPickerView *)pickerView
{
	return 2;
}

-(NSInteger) pickerView:(UIPickerView *)pickerView
numberOfRowsInComponent: (NSInteger)component
{
	if (component == 0)
		return [doData count];
	else {
		return [feelData count];
	}

}

- (NSString *)pickerView:(UIPickerView *)pickerView 
titleForRow:(NSInteger)row forComponent:(NSInteger)component
{
	if (component == 0)
	{
		return [doData objectAtIndex:row];
	}
	else {
		return [feelData objectAtIndex:row];
	}

}


/*
// The designated initializer. Override to perform setup that is required before the view is loaded.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
    }
    return self;
}
*/

/*
// Implement loadView to create a view hierarchy programmatically, without using a nib.
- (void)loadView {
}
*/



// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
	NSString *plistPath = [[NSBundle mainBundle] pathForResource:@"PickerData" ofType: @"plist"];
	NSDictionary *rootPicker = [NSDictionary dictionaryWithContentsOfFile:plistPath];
	doData = [[NSArray alloc] initWithArray: [rootPicker valueForKey:@"Do"]];
	feelData = [[NSArray alloc] initWithArray: [rootPicker valueForKey:@"Feel"]];
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
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
	self.doData = nil;
	self.picker = nil;
	self.feelData = nil;
	self.tweetItButton = nil;
}


- (void)dealloc {
	[doData release];
	[picker release];
	[feelData release];
	[tweetItButton release];
    [super dealloc];

}

@end
