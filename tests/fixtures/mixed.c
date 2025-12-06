// shared object with both global and static functions

static int helper(int x);
static int internal_calc(void);
static void cleanup(void);

int public_function(int x) {
    return helper(x) * 2;
}

int another_public(void) {
    return 42;
}

static int helper(int x) {
    return x + internal_calc();
}

static int internal_calc(void) {
    return 10;
}

static void cleanup(void) {}
