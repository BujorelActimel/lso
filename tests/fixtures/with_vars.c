// Shared object with functions and global variables

// global variables should not be listed by lso
int global_counter = 0;
const char* global_message = "Hello";
double global_pi = 3.14159;

void increment_counter(void) {
    global_counter++;
}

int get_counter(void) {
    return global_counter;
}

void reset_counter(void) {
    global_counter = 0;
}

static int internal_state = 0;

static void update_state(void) {
    internal_state++;
}
