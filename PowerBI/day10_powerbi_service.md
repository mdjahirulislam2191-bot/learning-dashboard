# দিন ১০: পাওয়ার বিআই সার্ভিস (Power BI Service) ☁️

## 🎯 আজকে যা শিখবেন
- Power BI Service (app.powerbi.com)
- রিপোর্ট পাবলিশ ও শেয়ারিং
- ড্যাশবোর্ড তৈরি
- অন-প্রিমাইস গেটওয়ে
- Schedule Refresh সেটআপ

## 📚 তাত্ত্বিক ধারণা

### Power BI Service কী?
Power BI Service হলো Microsoft-এর **ক্লাউড প্ল্যাটফর্ম** — এখানে আপনি আপনার Power BI Desktop-এ তৈরি রিপোর্ট **পাবলিশ** (আপলোড) করে অন্যদের সাথে শেয়ার করতে পারেন।

### Power BI আর্কিটেকচার

```
Power BI Desktop (✏️ Create)
     ↓  Publish
Power BI Service (☁️ Share)
     ↓  View
Power BI Mobile (📱 Consume)
```

### Power BI লাইসেন্সিং

| লেভেল | ফ্রি | Pro | Premium Per User (PPU) | Premium Capacity |
|-------|------|-----|------------------------|------------------|
| **খরচ** | ফ্রি | ~$10/মাস | ~$20/মাস | ~$5,000/মাস |
| **Share** | ❌ (শুধু My Workspace) | ✅ | ✅ | ✅ |
| **API** | ❌ | ✅ | ✅ | ✅ |
| **AI Features** | ❌ | ❌ | ✅ | ✅ |
| **XMLA Endpoints** | ❌ | ❌ | ✅ | ✅ |

### Key Terminology

| টার্ম | ব্যাখ্যা |
|-------|----------|
| **Workspace** | গুগল ড্রাইভের ফোল্ডারের মতো — রিপোর্টের গ্রুপ |
| **Dashboard** | ভিজুয়াল টাইলসের ক্যানভাস (এক পৃষ্ঠা) |
| **Report** | মাল্টি-পেজ ইন্টারঅ্যাকটিভ রিপোর্ট |
| **App** | প্যাকেজ করা কন্টেন্ট (ড্যাশবোর্ড + রিপোর্ট) |
| **Gateway** | লোকাল ডেটার সাথে ক্লাউডের সংযোগ |
| **Dataset** | আপনার ডেটা মডেল (PBIX-এর টেবিল) |
| **Schedule Refresh** | অটো ডেটা আপডেট |

---

## 💻 স্টেপ বাই স্টেপ: Power BI Service

### Step 1: Power BI Service-এ সাইন ইন
1. ব্রাউজার খুলুন → [app.powerbi.com](https://app.powerbi.com)
2. আপনার Microsoft Account (অফিস/স্কুল/ব্যক্তিগত) দিয়ে সাইন ইন করুন
3. প্রথমবার হলে, বিনামূল্যে সাইন আপ করুন

### Step 2: রিপোর্ট পাবলিশ (Power BI Desktop থেকে)

Power BI Desktop-এ:
1. **File** → **Publish** → **Publish to Power BI**
2. Target: **My Workspace** নির্বাচন করুন
3. **Select** ক্লিক করুন
4. Success Message দেখাবে → **Open 'MyWorkspace.pbix' in Power BI** ক্লিক করুন

### Step 3: Power BI Service-এ রিপোর্ট দেখা
1. **My Workspace** খুলুন
2. **Reports** ট্যাব → আপনার পাবলিশ করা রিপোর্ট দেখতে পাবেন
3. রিপোর্টের নাম ক্লিক করলে ইন্টারঅ্যাকটিভ রিপোর্ট ওপেন হবে

### Step 4: ড্যাশবোর্ড তৈরি

**একটি ড্যাশবোর্ড তৈরি করুন:**
1. রিপোর্ট ওপেন করুন
2. একটি ভিজুয়ালের উপর মাউস → **Pin Visual** 📌 আইকন
3. **Pin to Dashboard**:
   - Existing Dashboard বা
   - **New Dashboard** → নাম: "ফিন্যান্স ড্যাশবোর্ড"
4. **Pin** ক্লিক করুন

**ড্যাশবোর্ড কাস্টমাইজেশন:**
- টাইলগুলো ড্র্যাগ করে সাজান
- টাইল সাইজ পরিবর্তন করুন
- **Tile Details** থেকে সাবটাইটেল দিন

### Step 5: রিপোর্ট শেয়ারিং

**একটি রিপোর্ট শেয়ার করুন:**
1. রিপোর্ট ওপেন → **Share** বাটন (উপরের ডানে)
2. ইমেইল ঠিকানা দিন
3. Permission নির্বাচন করুন:
   - ✅ Allow recipients to share
   - ✅ Allow recipients to build content with the data
4. **Send** → রecipient ইমেইল পাবেন

**লিংক দিয়ে শেয়ার:**
1. **Share** → **Copy Link**
2. লিংক কপি করে মেসেঞ্জার/ইমেইলে পাঠান

### Step 6: Gateway সেটআপ (অন-প্রিমাইস ডেটার জন্য)

**কেন Gateway দরকার?**
আপনার লোকাল কম্পিউটারে Excel/CSV ফাইল থাকলে Power BI Service সরাসরি সেই ডেটা রিফ্রেশ করতে পারে না। Gateway দরকার।

**Gateway ইন্সটল:**
1. [Power BI Gateway ডাউনলোড](https://powerbi.microsoft.com/en-us/gateway/)
2. **Install** করুন **(Personal Mode)** — একজন ইউজারের জন্য
3. Gateway কী দিন (Power BI Service থেকে Generate করুন)

**Schedule Refresh সেটআপ:**
1. My Workspace → **Datasets** ট্যাব
2. ডেটাসেটের ⋮ → **Settings**
3. **Scheduled Refresh** → On ✅
4. Refresh Frequency: **Daily**
5. Time: আপনার পছন্দের সময় (যেমন: সকাল ৮টা)

### Step 7: Workspace তৈরি (টিমের জন্য)

**Workspace তৈরি:**
1. Workspaces → **Create workspace**
2. Name: "জাহিরুলের ফিন্যান্স অ্যানালাইসিস"
3. **Create**
4. **Access** → Members যোগ করুন (ইমেইল দিয়ে)

### Step 8: App পাবলিশ

১. Workspace-এ থাকা সব রিপোর্ট + ড্যাশবোর্ড তৈরি করুন
২. **Create app** বাটন ক্লিক করুন
৩. App Name: "পার্সোনাল ফিন্যান্স ড্যাশবোর্ড"
৪. Description: "জাহিরুলের মাসিক আয়-ব্যয় ট্র্যাকিং রিপোর্ট"
৫. Themes → আপনার পছন্দের থিম সিলেক্ট করুন
৬. Permissions → যাদের সাথে শেয়ার করবেন তাদের যোগ করুন
৭. **Publish app**

---

## 🧪 প্র্যাকটিস টাস্ক (Practice Tasks)

### টাস্ক ১: রিপোর্ট পাবলিশ
আপনার তৈরি করা ফিন্যান্স রিপোর্ট Power BI Service-এ পাবলিশ করুন। My Workspace-এ দেখুন।

### টাস্ক ২: ড্যাশবোর্ড তৈরি
ড্যাশবোর্ডে নিচের টাইলগুলো পিন করুন:
- Total Expense কার্ড
- Total Income কার্ড
- একটি চার্ট (মাসিক খরচ)
- ক্যাটাগরি ব্রেকডাউন পাই চার্ট

### টাস্ক ৩: ফিল্টার্ড ভিউ পিন করুন
একটি নির্দিষ্ট ফিল্টার্ড ভিউ পিন করুন (যেমন: শুধু "Food" ক্যাটাগরি)।

1. রিপোর্টে "Food" ফিল্টার করুন
2. Pin Visual 📌 → বিশেষ ফিল্টার সহ পিন হচ্ছে কিনা চেক করুন

### টাস্ক ৪: Schedule Refresh সেটআপ
Excel ফাইল থেকে ডেটা লোড করে থাকলে Schedule Refresh সেট করুন।

### টাস্ক ৫: শেয়ারিং টেস্ট
একজন সহকর্মী/বন্ধুর সাথে রিপোর্ট শেয়ার করুন। লিংক পাঠিয়ে নিশ্চিত হন যে তারা দেখতে পাচ্ছে।

### টাস্ক ৬: Power BI Mobile App
আপনার ফোনে Power BI Mobile App ইন্সটল করে আপনার ড্যাশবোর্ড দেখুন।

---

## 💡 ফিন্যান্স টিপস

### Cloud vs On-Premise — কখন কী?
| ডেটার উৎস | অন-প্রিমাইস | ক্লাউড |
|-----------|------------|--------|
| Excel (লোকাল) | ✅ | ❌ (Gateway দরকার) |
| SQL Server (লোকাল) | ✅ | ❌ (Gateway দরকার) |
| Excel Online (OneDrive) | ❌ | ✅ (Direct) |
| Google Sheets | ❌ | ✅ (Connector) |
| Web API | ❌ | ✅ (Direct) |

### Pro-Tips
1. ✅ **Dataset সেটিংসে** Refresh এ সময় জোন ঠিক করুন (Dhaka, UTC+6)
2. ✅ **Data Source Credentials** → Anonymous/Windows/Basic সঠিক সিলেক্ট করুন
3. ✅ **Dashboard Alerts** → টার্গেটের বেশি খরচ হলে Alert সেট করুন
4. ✅ **Comments** → টাইলসে কমেন্ট করে টিমের সাথে আলোচনা করুন
5. ✅ **Subscribe ক্লাস** → ইমেইলে রিপোর্ট পেতে Subscribe করুন

### Power BI Service Limitations (ফ্রি ভার্সন)
- ❌ ফ্রি ইউজার শুধু My Workspace-এ রিপোর্ট দেখতে পারে
- ❌ শেয়ার করতে Pro লাইসেন্স দরকার
- ❌ API Access নেই
- ❌ AI Insights নেই
- ✅ কিন্তু .pbix পাবলিশ ও নিজে দেখা যায়

---

## 📝 চূড়ান্ত চেকলিস্ট
- [ ] Power BI Service অ্যাকাউন্ট তৈরি করেছি
- [ ] Desktop থেকে Service-এ পাবলিশ করেছি
- [ ] রিপোর্ট ব্রাউজারে দেখতে পাচ্ছি
- [ ] ড্যাশবোর্ড তৈরি করেছি
- [ ] ড্যাশবোর্ডে টাইল পিন করেছি
- [ ] ফিল্টার্ড ভিউ পিন করেছি
- [ ] Schedule Refresh সেটআপ করেছি
- [ ] Gateway ইন্সটল করেছি (যদি দরকার হয়)
- [ ] রিপোর্ট শেয়ার করেছি
- [ ] Workspace তৈরি করেছি
- [ ] App পাবলিশ করেছি
- [ ] Power BI Mobile এ চেক করেছি

## 📖 অতিরিক্ত রিসোর্স
- [Microsoft Docs: Power BI Service](https://docs.microsoft.com/en-us/power-bi/fundamentals/service-basic-concepts)
- [Microsoft: Power BI Gateway](https://docs.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem)
- [Power BI Community](https://community.powerbi.com/)