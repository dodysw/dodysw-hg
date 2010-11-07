//
//  twitBlehAppDelegate.h
//  twitBleh
//
//  Created by Dody Suria Wijaya on 4/27/10.
//  Copyright __MyCompanyName__ 2010. All rights reserved.
//

#import <UIKit/UIKit.h>

@class twitBlehViewController;

@interface twitBlehAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    twitBlehViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet twitBlehViewController *viewController;

@end

