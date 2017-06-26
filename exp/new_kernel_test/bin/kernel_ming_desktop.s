	.file	"kernel.c"
	.section	.rodata
	.align 8
.LC0:
	.string	"you need to input the number of iterations you want run"
	.text
	.globl	main
	.type	main, @function
main:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$40, %rsp
	.cfi_offset 3, -24
	movl	%edi, -36(%rbp)
	movq	%rsi, -48(%rbp)
	cmpl	$2, -36(%rbp)
	je	.L2
	movl	$.LC0, %edi
	call	puts
	movl	$-1, %eax
	jmp	.L3
.L2:
	movq	-48(%rbp), %rax
	addq	$8, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	atoll
	movq	%rax, -24(%rbp)
	movq	$0, -32(%rbp)
	jmp	.L4
.L5:
#APP
# 31 "kernel.c" 1
	addl %eax, %eax 
	addl %ebx, %ebx 
	addl %ecx, %ecx 
	addl %edx, %edx 
	
# 0 "" 2
#NO_APP
	addq	$1, -32(%rbp)
.L4:
	movq	-32(%rbp), %rax
	cmpq	-24(%rbp), %rax
	jl	.L5
	movl	$0, %eax
.L3:
	addq	$40, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.1-2ubuntu1~16.04) 5.4.1 20160904"
	.section	.note.GNU-stack,"",@progbits
