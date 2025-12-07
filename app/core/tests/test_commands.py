"""test custom django management commands"""
#We will mock the behavior of the database because we need to be able to simulate when the database
#is returning a response or not.
from unittest.mock import patch
#And then we have this operational error exception, which we import from psycopg2.
#It's one of the possibilities of the errors that we might get when we try and 
#connect to the database before the database is ready.
from psycopg2 import OperationalError as Psycopg2Error
#Then we have the call command, which is a helper function provided by Django that
#allows us to simulate or to actually call a command by the name.
#And this allows us to actually call the command that we're testing.
from django.core.management import call_command
#And then we have another operational error, which is another exception that may 
#get thrown by the database depending on what stage of the start up process it is.
#And we basically want to cover both options.
from django.db.utils import OperationalError
#And then we have a simple test case, which is the base test course that we're 
#going to use for testing out our unit test or creating our unit test.
#And it's important that we use a simple test case because we are testing 
#behavior that the database is not available and therefore we do not need migrations
# and things like that to be applied to the test database because we're just 
#actually simulating behavior of that database.
#So we're just going to use simple test case so it doesn't create any database set up
# and things like behind the scenes.
from django.test import SimpleTestCase

class CommandTests(SimpleTestCase):
    """Test commands"""
    @patch('core.management.commands.wait_for_db.Command.check')
    def test_wait_for_db_ready(self,patched_check):
        """test waiting for database if database is ready"""
        #So this is one possible test case is that we run the way for DB command
        #and the database is already ready.So we don't want it to do anything.
        #We just want it to continue and allow us to get on with the execution 
        #of our application.So to do this, we need to mock the behavior of our database.
        #So we're going to mock that behavior by using patch using this 
        #"core.management.commands.wait_for_db.Command.check", and we're going 
        #to do it for all the different test methods.So we used the patch decorator.
        #And we're going to be mocking that check method to simulate the response so we 
        #can simulate that checkmethod, returning an exception, authorizing an exception,
        # and we can also simulate it.Returning a value.
        #So because we've added Patch here, it's going to add a new argument to each of the calls that we make
        #So we need to catch that here or we need to define, I should say, define the parameter as "patched_check"
        patched_check.return_value = True #"""this tell when we return check we return the true value"""
        call_command('wait_for_db') #"""this will execute the code inside our db"""
        patched_check.assert_called_once_with(databases=['default']) #"""this is for mocked value check inside our command 
        #is called with these parameters"""
    @patch('core.management.commands.wait_for_db.Command.check')
    @patch('time.sleep')
    def test_wait_for_db_delay(self,patched_sleep,patched_check): #"""So this is when there's a delay in starting, we want to simply check if the database is ready.
        #and the database is not ready so we will delay it for few seconds""":
        #Test waiting for database when getting operational error
        patched_check.side_effect = [Psycopg2Error]*2 + [OperationalError]*3 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count,6)
        patched_check.assert_called_with(databases=['default'])
        

