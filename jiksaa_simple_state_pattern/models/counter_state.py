from odoo.exceptions import ValidationError

from abc import ABC, abstractmethod


COUNTER_STATE_DRAFT = 'draft'
COUNTER_STATE_RUNNING = 'running'
COUNTER_STATE_DONE = 'done'
COUNTER_STATE_SELECTION = [
    (COUNTER_STATE_DRAFT, 'Draft'),
    (COUNTER_STATE_RUNNING, 'Running'),
    (COUNTER_STATE_DONE, 'Done'),
]


class AbstractCounterState(ABC):
    def __init__(self, counter):
        self.counter = counter

    @staticmethod
    def get_state(record):
        if record.state == COUNTER_STATE_DRAFT:
            return CounterStateDraft(record)
        elif record.state == COUNTER_STATE_RUNNING:
            return CounterStateRunning(record)
        elif record.state == COUNTER_STATE_DONE:
            return CounterStateDone(record)

    @abstractmethod
    def action_run(self):
        """
        Method triggering the counter run process

        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def action_done(self):
        """
        Method triggering the counter done process
        :return:
        :rtype:
        """
        pass

    @abstractmethod
    def action_count(self):
        """

        :return:
        :rtype:
        """
        pass


class CounterStateDraft(AbstractCounterState):
    def action_done(self):
        raise ValidationError('Draft Counter could not be set to Done')

    def action_run(self):
        self.counter.state = COUNTER_STATE_RUNNING

    def action_count(self):
        raise ValidationError('Counter should be running to perform this action')


class CounterStateRunning(AbstractCounterState):
    def action_done(self):
        self.counter.state = COUNTER_STATE_DONE

    def action_run(self):
        raise ValidationError('The counter is already running')

    def action_count(self):
        self.counter.value += 1


class CounterStateDone(AbstractCounterState):
    locked_error = 'Counter is locked'

    def action_done(self):
        raise ValidationError(self.locked_error)

    def action_run(self):
        raise ValidationError(self.locked_error)

    def action_count(self):
        raise ValidationError(self.locked_error)
