CREATE TABLE jk_counter_state (
  id serial,
  primary key(id)
);
CREATE TABLE counter_state_draft (primary key(id)) INHERITS (jk_counter_state);
CREATE TABLE counter_state_running (primary key(id)) INHERITS (jk_counter_state);
CREATE TABLE counter_state_done (primary key(id)) INHERITS (jk_counter_state);
