# 📘 Day 35: Equity — Free Cash Flow Models

## 🎯 শেখার উদ্দেশ্য

এই পাঠ শেষে আপনি যা পারবেন:
1. ফ্রি ক্যাশ ফ্লো (FCF) ধারণা বুঝতে
2. FCFF ও FCFE-এর পার্থক্য বুঝতে
3. FCF ভিত্তিক মূল্যায়ন মডেল বুঝতে
4. ডিভিডেন্ড-বিহীন কোম্পানি মূল্যায়ন করতে
5. FCF মডেলের সুবিধা ও অসুবিধা বুঝতে

---

## 📖 1. ফ্রি ক্যাশ ফ্লো কী?

**ফ্রি ক্যাশ ফ্লো:** কোম্পানির অপারেশন থেকে প্রাপ্ত নগদ যা পুনর্বিনিয়োগের পর অবশিষ্ট থাকে।

### FCFF (Free Cash Flow to Firm)
সকল মূলধন সরবরাহকারীর জন্য উপলব্ধ ক্যাশ (ঋণদাতা + শেয়ারহোল্ডার)।

### FCFE (Free Cash Flow to Equity)
শেয়ারহোল্ডারদের জন্য উপলব্ধ ক্যাশ (ঋণ পরিশোধের পর)।

---

## 📖 2. FCFF গণনা

**FCFF = CFO + Int(1-t) - CapEx**

**বা:** FCFF = NI + NCC + Int(1-t) - FCInv - WCInv

**যেখানে:**
- NI = Net Income
- NCC = Non-Cash Charges (Depreciation)
- Int = Interest Expense
- FCInv = Fixed Capital Investment (CapEx)
- WCInv = Working Capital Investment

**উদাহরণ:**
> CFO=$৫০০K, Interest=$৫০K, Tax=২৫%, CapEx=$৮০K
> FCFF = $৫০০K + $৫০K(০.৭৫) - $৮০K
> FCFF = $৫০০K + $৩৭.৫K - $৮০K = **$৪৫৭.৫K**

---

## 📖 3. FCFE গণনা

**FCFE = FCFF - Int(1-t) + Net Borrowing**

**বা:** FCFE = CFO - FCInv + Net Borrowing

**উদাহরণ:**
> CFO=$৫০০K, CapEx=$৮০K, Net Borrowing=$৩০K
> FCFE = $৫০০K - $৮০K + $৩০K = **$৪৫০K**

---

## 📖 4. FCF ভিত্তিক মূল্যায়ন

### ফার্ম ভ্যালু (Enterprise Value) — FCFF মডেল
`Firm Value = Σ FCFFt / (1+WACC)ᵗ`

**ইকুইটি ভ্যালু = ফার্ম ভ্যালু - মোট ঋণ**

### ইকুইটি ভ্যালু — FCFE মডেল
`Equity Value = Σ FCFEt / (1+r_e)ᵗ`

**স্থিতিশীল গ্রোথ:**
- FCFF: Firm Value = FCFF₁ / (WACC - g)
- FCFE: Equity Value = FCFE₁ / (r_e - g)

---

## ✍️ অনুশীলন

### প্রশ্ন ১:
FCFF = CFO($৪০০K) + Int(১-t)($৩০K×০.৭) - CapEx($১০০K) = ?

**সমাধান:**
FCFF = $৪০০K + $২১K - $১০০K = **$৩২১K**

### প্রশ্ন ২:
FCFE = FCFF($৩২১K) - Int(১-t)($২১K) + Net Borrowing($৫০K) = ?

**সমাধান:**
FCFE = $৩২১K - $২১K + $৫০K = **$৩৫০K**

### প্রশ্ন ৩:
DDM-এর চেয়ে FCF মডেল কেন পছন্দনীয়?

**উত্তর:** DDM শুধুমাত্র ডিভিডেন্ড প্রদানকারী কোম্পানির জন্য। FCF মডেল সব কোম্পানির জন্য ব্যবহার করা যায় — কোম্পানি ডিভিডেন্ড না দিলেও।

---

**পড়ার সময়:** ৪৫ মিনিট