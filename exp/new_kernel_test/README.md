Testing out a new kernel because of the large fluctuations observed for Tx

1) Testing out on two local machines in order to check the accuracy of the kernel (sanity check):
* Ming's Laptop
* Ming's Desktop

Here, we use the package `cpufrequtils` (requires sudo access) in order control the clock speed
Once we control the range of the clock speed, we use `perf state` to measure the execution of
the new kernel

2) Run this kernel on different remote machines in order to pinpoint where the fluctuations in Tx originate. (Running `/bin/sleep` confirmed that the problem is not with RP)
