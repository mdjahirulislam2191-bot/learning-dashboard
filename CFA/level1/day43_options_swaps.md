# 📘 Day 43: Derivatives — Options & Swaps

## 🎯 শেখার উদ্দেশ্য

এই পাঠ শেষে আপনি যা পারবেন:
1. কল ও পুট অপশন বুঝতে
2. অপশনের মৌলিক পরিভাষা বুঝতে
3. অপশনের পে-অফ বুঝতে
4. সোয়াপ চুক্তি বুঝতে
5. অপশন বনাম সোয়াপ বুঝতে

---

## 📖 1. অপশন (Options)

**অপশন:** একজন ক্রেতাকে একটি সম্পদ কেনার/বিক্রির অধিকার দেয় (বাধ্যবাধকতা নয়) নির্দিষ্ট দামে, নির্দিষ্ট সময়ের মধ্যে।

### কল অপশন (Call Option)
**ক্রেতা:** Strike Price-এ সম্পদ **কেনার** অধিকার
**বিক্রেতা (Writer):** Strike Price-এ সম্পদ **বিক্রি** করার বাধ্যবাধকতা

### পুট অপশন (Put Option)
**ক্রেতা:** Strike Price-এ সম্পদ **বিক্রি** করার অধিকার
**বিক্রেতা (Writer):** Strike Price-এ সম্পদ **কেনার** বাধ্যবাধকতা

---

## 📖 2. অপশন পরিভাষা

| পরিভাষা | বিবরণ |
|---------|--------|
| **Strike Price (Exercise Price)** | যে দামে সম্পদ কেনা/বেচা হবে |
| **Expiration Date** | অপশনের শেষ দিন |
| **Premium** | অপশনের দাম (প্রদেয়) |
| **In-the-Money (ITM)** | ব্যায়াম করলে লাভ |
| **At-the-Money (ATM)** | Strike = Market Price |
| **Out-of-the-Money (OTM)** | ব্যায়াম করলে লাভ নেই |

**ITM চার্ট:**
```
              Call            Put
ITM:        Strike < Market   Strike > Market
ATM:        Strike = Market   Strike = Market
OTM:        Strike > Market   Strike < Market
```

---

## 📖 3. অপশনের পে-অফ (Payoff)

**Call অপশন ক্রেতার পে-অফ:** max(০, S_T - X) - Premium
**Put অপশন ক্রেতার পে-অফ:** max(০, X - S_T) - Premium

**যেখানে:** S_T = মেয়াদে দাম, X = Strike Price

**উদাহরণ:**
> Strike $৫০, Premium $৩, মেয়াদে দাম $৬০
> Call Buyer Payoff = max(০, $৬০-$৫০) - $৩ = $১০ - $৩ = **$৭ লাভ ✅**

> Strike $৫০, Premium $৩, মেয়াদে দাম $৪০
> Put Buyer Payoff = max(০, $৫০-$৪০) - $৩ = $১০ - $৩ = **$৭ লাভ ✅**

---

## 📖 4. সোয়াপ (Swap)

**সোয়াপ:** দুই পক্ষের মধ্যে ভবিষ্যতের নগদ প্রবাহ বিনিময়ের চুক্তি।

### ইন্টারেস্ট রেট সোয়াপ (IRS)
সবচেয়ে সাধারণ সোয়াপ।

- **Fixed Rate Payer:** ফিক্সড রেট দেয়, ভেরিয়েবল রেট পায়
- **Floating Rate Payer:** ভেরিয়েবল রেট দেয়, ফিক্সড রেট পায়

**উদাহরণ:**
> কোম্পানি A-এর $১০M ঋণ আছে (Floating: LIBOR+১%)। কোম্পানি Fixed Rate চায়।
> কোম্পানি B-এর $১০M Fixed Rate ঋণ (৫%) আছে কিন্তু Floating চায়।
> তারা Swap করে: A B-কে ৫% দেয়, B A-কে LIBOR দেয়।
> নেটে: A = LIBOR+১% পায়, ৫% দেয় → শুধু ৪% (যদি LIBOR=৩%) — Fixed Rate effectively ৫%+স্প্রেড।

---

## ✍️ অনুশীলন

### প্রশ্ন ১:
Call Option Strike $৪০, Premium $৫, মেয়াদে দাম $৫৫ — মুনাফা/ক্ষতি কত?

**সমাধান:**
Payoff = max(০, $৫৫-$৪০) - $৫ = $১৫ - $৫ = **$১০ লাভ ✅**

### প্রশ্ন ২:
Swap-এ Fixed Rate Payer কখন উপকৃত হন?

**উত্তর:** যখন Market Interest Rate বেড়ে যায় — কারণ তিনি Fixed Rate পরিশোধ করছেন (কম) এবং Floating Rate পাচ্ছেন (বেশি)।

---

**পড়ার সময়:** ৪৫ মিনিট