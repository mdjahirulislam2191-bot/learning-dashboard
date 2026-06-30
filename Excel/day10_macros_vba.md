# দিন ১০: Macros & VBA — অটোমেশনের জগতে

## 🎯 আজকের লক্ষ্য
Excel ম্যাক্রো রেকর্ড করা এবং VBA (Visual Basic for Applications) এর মাধ্যমে কাজ অটোমেট করা শেখা।

## 🤖 ম্যাক্রো (Macro) কী?
ম্যাক্রো হলো Excel-এ রেকর্ড করা একটি অটোমেটেড কাজের ধারা — যা বারবার করা যায়।

## 📹 ম্যাক্রো রেকর্ড করা

### Developer Tab চালু করা
```
File → Options → Customize Ribbon → Main Tabs → ✅ Developer
```

### ম্যাক্রো রেকর্ডের ধাপ
```excel
1. Developer → Record Macro
2. Macro Name: দিন (যেমন: ফরম্যাট_রিপোর্ট)
3. Shortcut Key: (যেমন: Ctrl+Shift+R)
4. Store macro in: This Workbook
5. Description: কী কাজ করে তা লিখুন
6. OK → কাজ করুন → Stop Recording
```

### ✅ ম্যাক্রো দিয়ে কী কী অটোমেট করা যায়?
- ফরম্যাটিং (কালার, ফন্ট, বর্ডার)
- ফিল্টার ও সর্ট
- পিভট টেবিল রিফ্রেশ
- চার্ট তৈরি
- রিপোর্ট জেনারেট
- ডেটা কপি-পেস্ট
- ফাইল সেভ/প্রিন্ট

## 💼 ফাইন্যান্স ম্যাক্রো উদাহরণ

### উদাহরণ: মাসিক রিপোর্ট ফরম্যাট
```excel
ধাপসমূহ:
1. হেডার বোল্ড ও কালার দিন
2. কলামের প্রস্থ অটো-অ্যাডজাস্ট
3. সংখ্যায় কমা ফরম্যাট
4. বর্ডার যোগ করুন
5. ফিল্টার যোগ করুন
6. ফুটারে মোট যোগ করুন

ম্যাক্রো নাম: মাসিক_রিপোর্ট_ফরম্যাট
শর্টকাট: Ctrl+Shift+M
```

## 💻 VBA (Visual Basic for Applications)

### VBA এডিটর খোলা
```
Developer → Visual Basic
অথবা Alt + F11
```

### VBA প্রজেক্ট স্ট্রাকচার
```
Project Explorer:
├── Microsoft Excel Objects
│   ├── Sheet1 (Sheet1)
│   ├── Sheet2 (Sheet2)
│   └── ThisWorkbook
├── Modules
│   └── Module1
└── Forms
    └── UserForm1
```

## 📝 মৌলিক VBA সিনট্যাক্স

### Sub Procedure (ম্যাক্রো)
```vba
Sub ফরম্যাট_রিপোর্ট()
    ' এখানে কোড
    Range("A1").Font.Bold = True
    Range("A1").Interior.Color = RGB(0, 102, 204)
    Range("A1").Font.Color = vbWhite
End Sub
```

### ভেরিয়েবল ডিক্লেয়ারেশন
```vba
Dim বিক্রয় As Double
Dim নাম As String
Dim শেষ_সারি As Long
Dim ws As Worksheet

Set ws = ThisWorkbook.Sheets("Sheet1")
শেষ_সারি = ws.Cells(Rows.Count, 1).End(xlUp).Row
```

### ইফ-এলস স্টেটমেন্ট
```vba
If Range("B2").Value > 10000 Then
    Range("B2").Interior.Color = vbGreen
ElseIf Range("B2").Value > 5000 Then
    Range("B2").Interior.Color = vbYellow
Else
    Range("B2").Interior.Color = vbRed
End If
```

### লুপ (For Each)
```vba
Dim cell As Range
For Each cell In Range("A2:A100")
    If cell.Value > 10000 Then
        cell.Offset(0, 1).Value = "High"
    End If
Next cell
```

## 💼 ফাইন্যান্স VBA প্রোজেক্ট

### ১. অটোমেটিক ইনভয়েস নম্বর জেনারেটর
```vba
Sub নেক্সট_ইনভয়েস()
    Dim শেষ_সারি As Long
    Dim শেষ_নাম্বার As Long
    
    শেষ_সারি = Sheets("ডেটা").Cells(Rows.Count, 1).End(xlUp).Row
    শেষ_নাম্বার = Val(Mid(Sheets("ডেটา").Cells(শেষ_সারি, 1).Value, 2))
    
    Sheets("ইনভয়েস").Range("B2").Value = "INV-" & Format(শেষ_নাম্বার + 1, "00000")
End Sub
```

### ২. ক্যালকুলেটেড ফিল্ড যোগ করা
```vba
Sub লাভ_মার্জিন_যোগ()
    Dim শেষ_সারি As Long
    শেষ_সারি = Range("A" & Rows.Count).End(xlUp).Row
    
    Range("E1").Value = "লাভ মার্জিন"
    Range("E2:E" & শেষ_সারি).Formula = "=(D2-C2)/D2"
    Range("E2:E" & শেষ_সারี).NumberFormat = "0.00%"
End Sub
```

### ৩. ডেটা ভ্যালিডেশন চেক
```vba
Sub ডেটা_চেক()
    Dim cell As Range
    For Each cell In Range("B2:B100")
        If cell.Value = "" Then
            cell.Interior.Color = vbYellow
            cell.Comment.Text "মান বসানো হয়নি!"
        ElseIf Not IsNumeric(cell.Value) Then
            cell.Interior.Color = vbRed
            cell.Comment.Text "সংখ্যা দিন!"
        End If
    Next cell
End Sub
```

## 🎯 UserForm তৈরি (ইউজার ইন্টারফেস)

### ফর্ম তৈরি
```
Insert → UserForm
টুলবক্স থেকে:
- Label (লেবেল)
- TextBox (ইনপুট)
- ComboBox (ড্রপডাউন)
- CommandButton (বাটন)
```

### বাটনের ইভেন্ট কোড
```vba
Private Sub CommandButton1_Click()
    Dim বিক্রয় As Double
    Dim খরচ As Double
    
    বিক্রয় = CDbl(TextBox1.Value)
    খরচ = CDbl(TextBox2.Value)
    
    MsgBox "লাভ মার্জিন: " & Format((বিক্রয়-খরচ)/বিক্রয়, "0.00%")
End Sub
```

## ⚠️ সিকিউরিটি ও বেস্ট প্র্যাকটিস

### ম্যাক্রো সিকিউরিটি
```
File → Options → Trust Center → Trust Center Settings
- Disable all macros without notification
- Disable all macros with notification ✅ (প্রস্তাবিত)
- Enable all macros (বিপজ্জনক)
```

### VBA টিপস
- ✅ কোডে কমেন্ট যোগ করুন (') দিয়ে
- ✅ অর্থপূর্ণ নাম দিন (ফরম্যাট_রিপোর্ট, Not rpt1)
- ✅ On Error Resume Next দিয়ে এরর হ্যান্ডেল করুন
- ✅ Option Explicit ব্যবহার করুন
- ✅ .xlsm ফরম্যাটে সেভ করুন (ম্যাক্রো-ইনেবল্ড)
- ❌ অজানা উৎসের ম্যাক্রো রান করবেন না

## ✅ প্র্যাকটিস টাস্ক
1. Developer Tab চালু করুন (যদি না থাকে)
2. একটি সাধারণ ম্যাক্রো রেকর্ড করুন (হেডার ফরম্যাট)
3. VBA এডিটর খুলে কোড দেখুন
4. একটি Sub লিখুন যা:
   - শেষ সারে মোট যোগ করে
   - সংখ্যা ফরম্যাটিং করে
   - হেডার কালার করে
5. একটি লুপ লিখুন যা প্রতিটি সেল চেক করে
6. একটি মেসেজ বক্স তৈরি করুন

## 📝 টিপস
- **ম্যাক্রো রেকর্ডার** VBA শেখার সেরা উপায় — কাজ করুন, কোড দেখুন
- **Relative References** টগল করে রেকর্ড করুন (ডায়নামিক সিলেকশনের জন্য)
- F5 = Run, F8 = Step Through (ডিবাগ)
- **Immediate Window** (Ctrl+G) দিয়ে দ্রুত টেস্ট
- VBA কোড .xlsm ও .xlsb ফাইলেই কাজ করে

> **পরবর্তী দিন:** Excel-এ ড্যাশবোর্ড ডিজাইন!