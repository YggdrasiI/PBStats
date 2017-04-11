#ifndef __ASM_TEMPLATES_H__
#define __ASM_TEMPLATES_H__

/* Templates to modify of floats in releation to esp register.
 * Note: No evaluation, like 'OFFSET+4' in arguments allowed.
 * Note: Do not define locale variables in hooked function unless you also adapt the offset.
 * Note: __asm on each line is required because macro shrinks to single line.
 * Note: Do not add semicolon. Without ; the snippets can be nested.
 * */

/* Multiply float by float. */
#define FFMUL(OFFSET, FACTOR) \
    __asm{ \
        __asm 		fld [FACTOR] \
        __asm 		fmul DWORD PTR [esp+OFFSET] \
        __asm		fstp DWORD PTR [esp+OFFSET] \
    }

/* Multiply int with float scaling factor. */
#define IFMUL(OFFSET, FACTOR) \
    __asm{ \
        __asm 			fld [FACTOR] \
        __asm 		fimul DWORD PTR [esp+OFFSET] \
        __asm 			fistp DWORD PTR [esp+OFFSET] \
    }

/* Push integer on stack and multiply */
#define IFMUL_PUSH(REGISTER, FACTOR) \
    __asm{ \
        __asm push REGISTER \
        IFMUL(0, FACTOR) \
        __asm pop REGISTER \
    }

/* Add float value. */
#define FFADD(OFFSET, SHIFTVAR) \
    __asm{ \
        __asm 			fld [SHIFTVAR] \
        __asm 			fadd DWORD PTR [esp+OFFSET] \
        __asm 			fstp DWORD PTR [esp+OFFSET] \
    }

/* Add integer to integer value. */
#define IIADD(OFFSET, REG1, REG2, VALUE) \
    __asm{ \
        __asm 			mov REG1, [esp+OFFSET] \
        __asm 			mov REG2, [VALUE] \
        __asm 			add REG1, REG2 \
        __asm 			mov [esp+OFFSET], REG1 \
    }

#define IIADD8(OFFSET, VALUE) \
    __asm{ \
        __asm 			push eax \
        __asm 			push ecx \
        __asm 			mov eax, [esp+OFFSET] \
        __asm 			mov ecx, [VALUE] \
        __asm 			add eax, ecx \
        __asm 			mov [esp+OFFSET], eax \
        __asm 			pop ecx \
        __asm 			pop eax \
    }

/* Perform rescaling of (x,w) tupel a.k.a. reposition of left border of rect.
 *
 * iX, iW, fS given. Evaluate
 * w2 := fS * iW
 * x2 := x + ( iX - w2 )
 *
 * Require two registers.
 */
#define IIF_SCALE_LEFT(OFFSET_X, OFFSET_W, SCALEFACTOR, REG1, REG2) \
    __asm{ \
        __asm		mov REG1, [esp+OFFSET_W] \
        __asm		fld [SCALEFACTOR] \
        __asm		fmul DWORD PTR [esp+OFFSET_W] \
        __asm		fstp DWORD PTR [esp+OFFSET_W] \
        __asm		mov REG2, [esp+OFFSET_W] \
        __asm		sub REG1, REG2 \
        __asm		mov REG2, [esp+OFFSET_X] \
        __asm		sub REG2, REG1 \
        __asm		mov [esp+OFFSET_X], REG2 \
    }

#define COPY(OFFSET, REG, VALUE) \
    __asm{ \
        __asm mov REG, VALUE \
        __asm mov [esp+OFFSET], REG \
    }

#endif
