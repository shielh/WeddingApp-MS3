# Wedding App

This project was created for my third Milestone Project with Code Institute in order to display my knowledge and understanding 
of HTML, CSS, Python, Flask and MongoDB.

This project is definitely the one I am most excited about creating because it is for my sister for her wedding. She asked me a couple 
of months ago to make her a site where her wedding guests could RSVP, register, log in and see all of the information they need to know 
about her big day as well as allowing them to submit any dietary requirements or accessibility issues. This site will allow her to relax 
in the leadup to her big day knowing that all the guests data will be stored in the one place for her to view rather than sending multiple 
emails to find out the information.

This is my first project where I will be getting instructions from my sister on the features and content needed on this site and I think it 
will be a great learning curve for what I can expect when I start working as a Web Developer.

---

## Table of Contents
* [User Experience](#User-Experience)
    * [The Strategy Plane](#The-Strategy-Plane)
        * [User stories](#User-Stories)
    * [The Scope Plane](#The-Scope-Plane)
    * [The Structure Plane](#The-Structure-Plane)
    * [The Skeleton Plane](#The-Skeleton-Plane)
        * [Wireframes](#Wireframes)
        * [Database Design](#Database-Design)
    * [The Surface Plane](#The-Surface-Plane)
        * [Design](#Design)
            * [Colour Scheme](#Colour-Scheme)
            * [Typography](#Typography)
            * [Imagery](#Imagery)
* [Features](#Features)
    - [Future Features to Implement](#future-features-to-implement)
* [Technologies Used](#Technologies-Used)
* [Testing](#testing)
    - [Responsivity across devices](#responsivity-across-devices)
    - [HTML and CSS validation](#html-and-css-validation)
    - [User Stories](#user-stories)
    - [Manual Testing](#manual-testing)
 * [Issues and Solutions](#issues-and-solutions)   
* [Deployment](#deployment)
    * [Initial Creation](#initial-creation)
    * [Deployment to Heroku](#deployment-to-heroku)
        - [Create the app on Heroku](#create-the-app-on-heroku)
        - [Connect Heroku to Github](#connect-heroku-to-github)
        - [Set environment variables](#set-environment-variables)
        - [Automatic Deployment](#automatic-deployment)
* [Credits](#credits)
    * [Content](#content)
    * [Media](#media)
    * [Acknowledgements](#acknowledgements)

--- 

## User Experience
### The Strategy Plane
Weddings can be extremely stressful to plan. There is so much to think about in the run up to the big day like the flowers, the table plans, 
the guests dietary requirements. The list goes on. For my sister, whose wedding is next September, she wanted a place where her guests could 
register, login, have access to all the information about their wedding and have the ability to add a variety of special requests ranging 
from dietary requirements to wanting to stay on the property in Italy.

This project was created for my sister Emma for her big day to help alleviate some of the stress. The aim is to provide a simple web 
application where wedding guests can add, edit and delete their specific requirements.

### User Stories
* As a user, I want to be able to easily navigate across the site so I can find the content quickly
* As a user, I want to view a pretty website with images of the wedding venue
* As a user, I want to be able to register an account so I can add any required information the bride might need
* As a user, I want to be able to update or delete the information I add
* As a user, I want to be able to find out all the information about the wedding; the dates, the venue, the schedule
* As a user, I want the website to be responsive across all devices

### The Scope Plane
#### Features on site
* index.html page detailing the wedding venue, dates and itinerary to people who have registered an account
* index.html page detailing a hero image with anchor tags to the register or log in pages
* accommodation.html page giving information about the rooms and the local area
* Burger icon menu on mobile devices
* Register, login and logout functionality
* preferences.html where guests (when logged in) can add preferences
* CRUD functionality for these preferences
* Modal dialog box for delete functionality to add defensive programming 
* MongoDB to store wedding guest information and user login details

### The Structure Plane
User Story:
 As a user, I want to be able to easily navigate across the site so I can find the content quickly

Acceptance Criteria:
* Navigation bar to be displayed across all pages on the site
* Navigation links all render the correct pages
* Mobile users will see a burger icon for the dropdown menu

Implementation:
A navigation bar will be displayed on the top of each page of the site.
The navigation links will each bring the user to the appropriate pages.
In mobile view, a collapsible burger icon will detail the menu items to the user.

This is a list of the navigation items that will be visible when not logged in:
* Home - index.html
* Log In - login.html
* Register - register.html

This is a list of the navigation items that will be visible while logged in:
* Home - index.html
* Accommodation - accommodation.html
* Preferences - preferences.html
* FAQ - faq.html
* Log Out -(Redirects to Log In page)

User Story:
 As a user, I want to view a pretty website with images of the wedding venue

Acceptance Criteria:
* Images to be displayed across the site

Implementation:


### The Skeleton Plane
#### Wireframes
The desktop version wireframes for this project can be found [here](Mockups/Desktop) and the mobile version can be found [here](Mockups/Mobile)

#### Database Schema
The application uses three collections named user, guest_info and update. The following are made up examples<br>
<pre>Collection: user 
{
    firstName: John
    lastName: Doe
    email: johndoe@gmail.com
    password: abcd1234
    is_admin: false
}
</pre>
<pre>Collection: guest_info
{
    number_of_party: 1 
    require_accommodation: yes
    dietary_restrictions: yes
    dietary_restrictions_description: Gluten free
    arrival_date: 08/09/2022
    add_note: Really looking forward to it
    created_by: johndoe@gmail.com
}</pre>
<pre>Collection: update
{
    number_of_party: 1 
    require_accommodation: yes
    dietary_restrictions: yes
    dietary_restrictions_description: Gluten free
    arrival_date: 08/09/2022
    add_note: Really looking forward to it
    created_by: johndoe@gmail.com
}</pre>


## Deployment 
### Initial Creation
Wedding App was first created by completing the following steps on GitHub:
1. Open [Github](https://github.com/) page up in browser
2. Log in using your username and password
3. Click the "New" green button to the left-hand side repository section
4. Click template dropdown menu and select the "Code Institute Full Template"
5. Enter name of project "WeddingApp-MS3"
6. Click "Create repository"
7. Click the green "Gitpod" button ONCE to redirect to the Gitpod workspace
8. Open via [Gitpod Workspaces](https://gitpod.io/workspaces/) only, from then on

Throughout development, three primary commands were used with the CLI [Git](https://git-scm.com/) and were as follows :

- "git add" followed by the file name you wish to stage or "git add ." stages all unstaged files
- "git commit -m" followed by a detailed comprehensive comment pertaining to the changes made since the previous commit
- "git push" makes all changes visible on the GitHub Repo

### Deployment to Heroku
#### Create the app on Heroku
1. Navigate to [Heroku](https://www.heroku.com) and login using your credentials
2. Click on the "New" button in the top right hand corner and select create new app
3. Enter the app name and select "Europe" for the region

#### Connect Heroku to Github
1. Click on the "Deploy" tab and select "GitHub", then "Connect to GitHub"
2. Box appears to find a github repository to connect to
3. Enter the repo name created on Github, in this case "WeddingApp-MS3"
4. Then click search
5. When the correct repo has been found, click the button to connect

#### Set environment variables
In Heroku, click on the "Settings" tabe and click "Reveal Config Vars" button to add the following information:
1. key: IP, value: 0.0.0.0
2. key: MONGO_DBNAME, value: database name(wedding_app)
3. key: MONGO_URI, value: (This value is found in Mongo DB by accessing "clusters" then "connect" then "connect to your application". You have to 
add in your own database name and password also)
4. key: PORT, value: 5000
5. key: SECRET_KEY, value: (Used to keep the site secure)

#### Automatic deployment
Click on the "deploy" tab and choose the branch you wish to deploy. Then, click "Enable Automatic Deploys"