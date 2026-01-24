# 🔧 SIDEBAR FIX: Rename Page Files

## 🎯 The Problem

The sidebar wasn't appearing because Streamlit requires specific file naming conventions for multi-page apps to automatically display pages in the sidebar.

## ✅ The Solution

Rename the page files with **number prefixes and emoji icons**. This tells Streamlit:
1. The order of pages in the sidebar
2. What to display as the page name

## 📝 File Name Changes

### OLD Names (Won't Show in Sidebar):
- ❌ `pages/simulation.py`
- ❌ `pages/cognitive_demo.py`
- ❌ `pages/institutional_behavior.py`
- ❌ `pages/viz_3d.py`

### NEW Names (Will Show in Sidebar):
- ✅ `pages/1_📊_Simulation.py`
- ✅ `pages/2_🧠_Cognitive_Demo.py`
- ✅ `pages/3_🏛️_Institutional_Behavior.py`
- ✅ `pages/4_🌍_3D_Visualization.py`

## 🚀 How to Deploy

### Option 1: Download and Replace (Easiest)

1. **Download the 4 renamed files** (provided below)
2. **Delete old page files** from your `pages/` directory:
   - Delete `simulation.py`
   - Delete `cognitive_demo.py`
   - Delete `institutional_behavior.py`
   - Delete `viz_3d.py`

3. **Add the new files** to your `pages/` directory:
   - Add `1_📊_Simulation.py`
   - Add `2_🧠_Cognitive_Demo.py`
   - Add `3_🏛️_Institutional_Behavior.py`
   - Add `4_🌍_3D_Visualization.py`

4. **Push to GitHub**:
```bash
cd /path/to/auracelle-bach
git add pages/
git commit -m "Fix: Rename pages for sidebar navigation"
git push
```

### Option 2: Rename Manually

If you prefer to rename files yourself:

**On macOS/Linux:**
```bash
cd pages/
mv simulation.py "1_📊_Simulation.py"
mv cognitive_demo.py "2_🧠_Cognitive_Demo.py"
mv institutional_behavior.py "3_🏛️_Institutional_Behavior.py"
mv viz_3d.py "4_🌍_3D_Visualization.py"
```

**On Windows (PowerShell):**
```powershell
cd pages
Rename-Item simulation.py "1_📊_Simulation.py"
Rename-Item cognitive_demo.py "2_🧠_Cognitive_Demo.py"
Rename-Item institutional_behavior.py "3_🏛️_Institutional_Behavior.py"
Rename-Item viz_3d.py "4_🌍_3D_Visualization.py"
```

**On Windows (File Explorer):**
1. Navigate to `pages/` folder
2. Right-click each file → Rename
3. Use the new names exactly as shown above (including emojis!)

## 📂 Final Directory Structure

```
auracelle-bach/
├── app.py
├── bach_api_utils.py
├── moral_foundations.py
├── trust_dynamics.py
├── pages/
│   ├── 1_📊_Simulation.py          ← NEW
│   ├── 2_🧠_Cognitive_Demo.py       ← NEW
│   ├── 3_🏛️_Institutional_Behavior.py ← NEW
│   └── 4_🌍_3D_Visualization.py     ← NEW
├── requirements.txt
└── README.md
```

## 🎯 How Streamlit Naming Works

Streamlit looks for files in the `pages/` directory with this pattern:

**Pattern**: `[number]_[emoji]_[Page Name].py`

- **Number** (optional): Controls sort order (1, 2, 3, 4)
- **Emoji** (optional): Shows in sidebar
- **Page Name**: Displayed text (underscores become spaces)

**Examples:**
- `1_📊_Simulation.py` → Shows as "📊 Simulation" (1st in list)
- `2_🧠_Cognitive_Demo.py` → Shows as "🧠 Cognitive Demo" (2nd in list)
- `About.py` → Shows as "About" (no number/emoji)

## ✅ Expected Result

After deploying the renamed files, you'll see:

### In the Sidebar:
```
📊 Simulation
🧠 Cognitive Demo
🏛️ Institutional Behavior
🌍 3D Visualization
```

### How It Works:
1. Login with `charlie2025`
2. See welcome message
3. **👈 Look at left sidebar** - Pages now visible!
4. Click any page to navigate
5. All pages work with full functionality

## 🔍 Verification

Check that your `pages/` directory has:
- [ ] `1_📊_Simulation.py` (not simulation.py)
- [ ] `2_🧠_Cognitive_Demo.py` (not cognitive_demo.py)
- [ ] `3_🏛️_Institutional_Behavior.py` (not institutional_behavior.py)
- [ ] `4_🌍_3D_Visualization.py` (not viz_3d.py)
- [ ] NO old files without number prefixes

## 🆘 Troubleshooting

### "Sidebar still not showing"
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check file names match EXACTLY (including emojis)
- Ensure files are in `pages/` directory (not root)
- Restart Streamlit: On Streamlit Cloud, click "Reboot app"

### "Emojis not displaying correctly"
- Files should be saved as UTF-8 encoding
- Emojis should work on all platforms (Windows/Mac/Linux)
- If problems persist, you can use simple names: `1_Simulation.py`

### "Pages showing in wrong order"
- Check the number prefixes (1, 2, 3, 4)
- Streamlit sorts alphabetically by filename
- Numbers ensure correct order

### "Import errors on pages"
- Make sure file contents didn't change, only the filenames
- Verify `bach_api_utils.py`, `moral_foundations.py`, `trust_dynamics.py` are in root

## 📊 Why This Matters

Streamlit's auto-discovery for multi-page apps requires specific naming:

**Without proper naming:**
- ❌ Pages don't appear in sidebar
- ❌ Users can't navigate
- ❌ App seems broken

**With proper naming:**
- ✅ Sidebar automatically appears
- ✅ Pages listed in order
- ✅ Beautiful emoji icons
- ✅ Professional navigation

## 🎉 Success!

After this fix:
1. ✅ Login page works
2. ✅ Authentication successful
3. ✅ **Sidebar appears with all 4 pages**
4. ✅ Click any page to navigate
5. ✅ Full Auracelle Bach functionality

---

**Files to Upload**: 4 renamed page files (provided below)

**Time to Deploy**: ~1 minute on Streamlit Cloud

**Result**: Beautiful sidebar navigation! 🎊
