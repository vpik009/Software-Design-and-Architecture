from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""

from datetime import datetime, timedelta
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""




class ContractState(ABC):
    '''
    An interface implemented by all the possible states a contract can be in (concrete state classes).
    '''


    @abstractmethod
    def doState(self, contract):
        '''
        abstract method to be implemented by concrete state classes
        :param1 contract: the instance of the contract that the method is to run on
        '''
        pass

    @abstractmethod
    def type(self) -> str:
        '''
        method that returns a string specifying the state of contract
        '''
        pass

    @abstractmethod
    def _notify(self) -> str:
        '''
        method used to generate the notification string
        '''
        pass



class PendingContractState(ContractState):


    def __init__(self):
        '''
        an empty constructor
        '''
        pass

    def type(self):
        '''
        method that returns the type of state as a string
        '''
        return "pending"

    def doState(self, contract):
        '''
        doState method that performs the actions of the current state and sets the next contract state accordingly
        :output: returns the string to be displayed as a notification or None if nothing is to be displayed
        :contract: the contract that holds the state
        '''

        # the user cannot renew the contract when it is in this state. Hence can only be expiring or expired

        ret = None

        if contract.getDateSigned() is not None:  # if the contract was signed
            contract.setState(ValidContractState())  # the contract is expired.
            ret = contract.doState()


        else:
            # keep it the same state (cannot renew if expiring, hence this is the only option)
            print(contract.getDateSigned())
            ret = self._notify(contract)

        return ret

    def _notify(self, contract):
        '''
        Private method that returns the state's notification message as a string
        :contract: the contract that holds the state
        '''
        return "Contract with ID:"+contract.getId()+"\n is currently pending a signature from the tutor"

class ExpiringContractState(ContractState):


    def __init__(self):
        '''
        an empty constructor
        '''
        pass

    def type(self):
        '''
        method that returns the type of state as a string
        '''
        return "expiring"

    def doState(self, contract):
        '''
        doState method that performs the actions of the current state and sets the next contract state accordingly
        :output: returns the string to be displayed as a notification or None if nothing is to be displayed
        :contract: the contract that holds the state
        '''

        # the user cannot renew the contract when it is in this state. Hence can only be expiring or expired

        time_now = datetime.now()
        ret = None

        if contract.getExpiryDate() <= time_now:
            contract.setState(ExpiredContractState())  # the contract is expired.
            ret = contract.doState()

        # elif contract.getExpiryDate() <= datetime.now()+timedelta(days=30):  # if less than or equal to one month to expiry date
        #     return ExpiringContractState()

        else:
            # keep it the same state (cannot renew if expiring, hence this is the only option)
            ret = self._notify(contract)

        return ret

    def _notify(self,contract):
        '''
        Private method that returns the state's notification message as a string
        :contract: the contract that holds the state
        '''
        expire_in = contract.getExpiryDate() - datetime.now()
        return "Contract with id:"+contract.getId()+"\nwill expire in:"+str(expire_in)

class ExpiredContractState(ContractState):


    def __init__(self):
        '''
        an empty constructor
        '''
        pass

    def type(self):
        '''
        method that returns the type of state as a string
        '''
        return "expired"

    def doState(self, contract):
        '''
        doState method that performs the actions of the current state and sets the next contract state accordingly
        :output: returns the string to be displayed as a notification or None if nothing is to be displayed
        :contract: the contract that holds the state
        '''

        time_now = datetime.now()
        ret = None

        if contract.getExpiryDate() <= time_now:
            ret = ""  # the contract is expired. No notifications to display
        elif contract.getExpiryDate() <= (time_now + timedelta(days=30)):  # if less than or equal to one month to expiry date
            contract.setState(ExpiringContractState())  # contract has been renewed
            ret = contract.doState()
        else:
            contract.setState(ValidContractState()) # contract has been renewed
            ret = contract.doState()

        return self._notify(contract)

    def _notify(self,contract):
        '''
        Private method that returns the state's notification message as a string
        :contract: the contract that holds the state
        '''
        return "Contract with ID:"+contract.getId()+"\nis EXPIRED"

class ValidContractState(ContractState):


    def __init__(self):
        '''
        an empty constructor
        '''
        pass

    def type(self):
        '''
        method that returns the type of state as a string
        '''
        return "valid"

    def doState(self, contract):
        '''
        doState method that performs the actions of the current state and sets the next contract state accordingly
        :output: returns the string to be displayed as a notification or None if nothing is to be displayed
        :contract: the contract that holds the state
        '''

        time_now = datetime.now()

        ret = None

        if contract.getExpiryDate() <= time_now:
            contract.setState(ExpiredContractState())  # the contract is expired.
            ret = contract.doState()
        elif contract.getExpiryDate() <= time_now+timedelta(days=30):  # if less than or equal to one month to expiry date
            contract.setState(ExpiringContractState())
            ret = contract.doState()
        else:
            ret = self._notify(contract)

        return ret

    def _notify(self, contract):
        '''
        Private method that returns the state's notification message as a string
        :contract: the contract that holds the state
        '''
        expire_in = contract.getExpiryDate() - datetime.now()
        return "Contract with ID:" + contract.getId() + "\nwill expire in:" + str(expire_in)