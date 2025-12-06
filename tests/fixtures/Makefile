CC = gcc
CFLAGS = -fPIC -Wall
LDFLAGS = -shared

TEST_SOS = simple.so mixed.so with_vars.so empty.so

all: $(TEST_SOS)

%.so: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

clean:
	rm -f *.so

.PHONY: all clean
