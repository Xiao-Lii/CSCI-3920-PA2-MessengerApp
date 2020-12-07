## CSCI 3920 - Advanced Programming w/ Python: PA2 Messenger App

### Summary
A Client — Server multithreading system for a messaging system like Slack, MS Teams, etc. The system will consist of two applications: the messenger system and a messaging client. The messenger system will run a server to maintain users and relay messages between the users. The messaging client connects to the messenger system, sign in the user and allow to send and receive messages. 


Users in the platform will have a username, password and display name. A user can send a direct message to another user by knowing his/her username. The messenger system will relay the message as soon as possible. However, if the message target user is not connected at that time, the message will be stored and the server will keep trying to relay the message. 

### Notes about the program
* We don't have a phone number variable for sign up, instead we used display_name
    * Phone number was not used in any function based on the project details
        * On 2.2.1 #1a has the protocol USR|username|password|display_name, hence the reason we omit phone number and used display_name
        
* .json file loads properly and allows the user to sign it with the credentials provided in the file, but unable to send message.
    * Shows this error: TypeError: put() missing 1 required positional argument: 'item' under self.__outgoing_messages.put(message_to_send)
    
* If .json file is not loaded, and the user created new accounts it the new accounts can send and receive messages.
####To start the program:
* Run Server:
    * The Server Main Menu will be displayed and prompts the user to either: 
         * Load data from file
            * user needs to input the filename: database
            * The .json file loads correctly.
        * Start the messenger service
            -* The server will run and will wait until it receives a connection from client


* Run Client:
    * Connect to server
        * User will be asked to enter a port number for the background client worker
        * User can enter a port number after 10000, which is the port number for the server
             * We used 10001,10002,10003... for background port when testing.
                
    * Login
        * User will have a choice to either sign in or sign up.
            * Usernames we already have on database:
                - username: user password:pw
                - username: user2 password:pw
            * To sign up or create an account the program will ask the user to enter the following:
                - username | password | email
                - Once the user signs up and there's no duplicates, it will display success message.
                - If the user sign up a new account the user need to choose option 2. Login > 1. Login existing user to sign in and use the messenger system
        
    * Send message:
        * User will be prompt to enter the username they wish to send message to.
            * An error message will appear if the username entered is not in the system.
            * If the username is in the system the user can send a message
                * Once the message is sent the user will see a message "Message {message_number} sent successfully"
                * If the recepient logs in they will see this message:
                    * [BG.CLIENT] [SERVER NOTIFICATION] R|{sender}|{message_number}|{message}
                    * [BG.CLIENT] [BG.CW] 0|{message_number}
                        
* Menu will continue to show until the user decided to disconnect or quit.
            
    
### ----------- Team Members -----------
    Xiao-Lii    -   Lee Phonthongsy
    rinv12      -   Rin(Loureen) Viloria 
    rrk01       -   Rizzul(Ryan Karki)
