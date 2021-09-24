
# About

The application is aimed at allowing tutors and students to log in to their accounts and find relevant tutors through the creation of tutor requests. As well as to allow tutors to find tutoring opportunities in their subject by displaying their relevant tutor requests from students and allowing them to bid on the request or accept it, in which case, the application creates a contract between the student and the tutor for the specified amount of time.
	
- As a student, you can create requests (as a bid) for tutors by including the subject and level of tutor competency in the specified subject that you require.
- As a tutor, you can view bids, create counteroffers, and accept bids from students that are available to you.
- The application keeps a record of the contracts between tutors and students and notifies the users about their expiration date.
	
The application was developed in python using Tkinter GUI. The main focus of this project was to develop this application using an object-oriented approach utilizing SOLID object-oriented programming principles and various design patterns to keep the application maintainable and extensible throughout the development process.


### Running the application:

	Run the Application.py file to run the UI.



### NOTES:

	Creating bids: Only a student has an option to do so
	Making offers: Not all tutors can see all the student's offers. Only those with high enough competency in the requested subject.
	If an incorrect API key is entered the first time, you will have to restart the application and retry since the API key is saved with singleton
