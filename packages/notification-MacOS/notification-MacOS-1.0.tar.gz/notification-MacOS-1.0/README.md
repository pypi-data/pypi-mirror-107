 ## Notification-macOS


Create and send custom notifications for macOS, add a title, subtitle, description and notification sound. 

Example:

```
import notifications-macOS

Notify = Notification(title='notification!', text='hello', Sound='Ping',)

Notify.send()
```

Use `Notify.send()` to send the notification                                                                                                       

Use `Notify.modify()` to modify the variables in the notification

Use `Notify.get_sounds()` to get a list of the available notification sounds


> Recommended: MacOS 10.12 or higher 

