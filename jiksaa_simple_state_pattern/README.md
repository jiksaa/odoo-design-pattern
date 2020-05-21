# State Design Pattern

This module implements the State design pattern in a traditional way using
Python classes without any Odoo ORM.

## Use Case

To demonstrate the State pattern the module defines the `jk.simple.counter` model
having the following state workflow:

            +-------------------------------------------------+
            |                                                 |
            | +----+----+      +-----------+      +----+---+  |
            | |         | run  |           | lock |        |  |
            | |  draft  +----->+  running  +----->+  done  |  |
            | |         |      |           |      |        |  |
            | +---------+      +-+-------+-+      +--------+  |
            |                    |       ^                    |
            |                    +-------+                    |
            |                      count                      |
            |                                                 |
            +---------------+----------------+----------------+
                            |                ^
                            +----------------+
                                  notify

Therefore, we get 3 states having action methods allowing records to switch to other state.
Unlike the other actions, `notify` could be performed at any states.

## Implementation

The `jk.simple.counter` model defined its states in the typical Odoo fashion using a `state` selection field
defined as follow:


    COUNTER_STATE_DRAFT = 'draft'
    COUNTER_STATE_RUNNING = 'running'
    COUNTER_STATE_DONE = 'done'
    COUNTER_STATE_SELECTION = [
        (COUNTER_STATE_DRAFT, 'Draft'),
        (COUNTER_STATE_RUNNING, 'Running'),
        (COUNTER_STATE_DONE, 'Done'),
    ]
    
    state = fields.Selection(
        selection=COUNTER_STATE_SELECTION,
        string='State',
        default=COUNTER_STATE_DRAFT,
        required=True
    )

The states logic is defined with the following structure:
    
                          +-----------------------------+
                          |    AbstractCounterState     |
                          +-----------------------------+
                          | counter: jk.simple.counter  |
                          |                             |
                          | static get_state(record)    |
                          | abstract action_run()       |
                          | abstract action_done()      |
                          | abstract action_count()     |
                          |                             |
                          +---------------+-------------+
                                          ^
                                          |
              +------------------------------------------------------+
              |                           |                          |
    +---------+---------+      +----------+----------+     +---------+--------+
    | CounterDraftState |      | CounterRunningState |     | CounterDoneState |
    +-------------------+      +---------------------+     +------------------+
    +-------------------+      +---------------------+     +------------------+
    
The `AbstractCounterState` class defined abstract methods that every subclasses should implements
and therefore handle. The class also defines a static method allowing the create a concrete instance
according to the given `jk.simple.counter` record given as method argument.

Each state has a reference to a `jk.simple.counter` instance allowing alter its
state.

On the `jk.simple.counter` implementation, the same methods are defined and their implementation always
follow the same logic: retrieve its corresponding state instance through the `AbstractCounterState` static
method then call the corresponding method on it.

Actions having the same logic regardless of counter state could be defined directly in the model class.

## Pros & Cons

TODO

## State Pattern References

- [https://www.geeksforgeeks.org/state-design-pattern/](https://www.geeksforgeeks.org/state-design-pattern/)
- [https://sourcemaking.com/design_patterns/state](https://sourcemaking.com/design_patterns/state)