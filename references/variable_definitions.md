# Variable Definitions

## Dataset

**Source:** Youth Risk Behavior Survey (YRBS 2007)

**Population:** American adolescents.

---

# Response Variable

## MultipleSexPartners

### Original Question

During your life, with how many people have you had sexual intercourse?

### Original Responses

| Code | Response |
|------|----------|
| A (1) | Never had sexual intercourse |
| B (2) | 1 person |
| C (3) | 2 people |
| D (4) | 3 people |
| E (5) | 4 people |
| F (6) | 5 people |
| G (7) | 6 or more people |

### Recoding

- Never had sexual intercourse → Missing
- 1 person → Missing
- 2 or more people → Numerical scale

### Role

Response (dependent) variable.

---

# Predictor Variables

## TaughtAboutHIV

### Original Question

Have you ever been taught about AIDS or HIV infection in school?

### Original Responses

| Code | Response |
|------|----------|
| A (1) | Yes |
| B (2) | No |
| C (3) | Not sure |

### Recoding

- Yes = 1
- No = 0
- Not sure = Missing

---

## HIVTesting

### Original Question

Have you ever been tested for HIV, the virus that causes AIDS?

### Original Responses

| Code | Response |
|------|----------|
| A (1) | Yes |
| B (2) | No |
| C (3) | Not sure |

### Recoding

- Yes = 1
- No = 0
- Not sure = Missing

---

## CondomUse

### Original Question

The last time you had sexual intercourse, did you or your partner use a condom?

### Original Responses

| Code | Response |
|------|----------|
| A (1) | Never had sexual intercourse |
| B (2) | Yes |
| C (3) | No |

### Recoding

- Yes = 1
- No = 0
- Never had sexual intercourse = Missing

---

# Statistical Model

Response variable:

- MultipleSexPartners

Predictor variables:

- TaughtAboutHIV
- HIVTesting
- CondomUse
