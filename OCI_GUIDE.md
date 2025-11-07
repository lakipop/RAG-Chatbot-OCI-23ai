# Complete Setup Guide - OCI RAG Chatbot

This guide will walk you through setting up Oracle Cloud Infrastructure (OCI) and Oracle Database 23ai for this RAG chatbot project.

---

## Part 1: Create Oracle Cloud Account

### Step 1: Sign Up for OCI Free Tier
1. Go to: https://www.oracle.com/cloud/free/
2. Click **"Start for free"**
3. Fill in your details (email, country, name)
4. Verify your email and phone number
5. Add a payment method (won't be charged - it's for verification only)
6. Choose your **Home Region** (pick one close to you - **you cannot change this later**)

**Important:** OCI Free Tier gives you:
- Always Free resources (never expire)
- $300 USD free credits for 30 days
- Free Oracle 23ai Autonomous Database

---

## Part 2: Set Up Oracle Autonomous Database 23ai

### Step 1: Create Your Database
1. Log in to Oracle Cloud: https://cloud.oracle.com/
2. Click the **hamburger menu** (☰) top-left
3. Go to: **Oracle Database** → **Autonomous Database**
4. Click **"Create Autonomous Database"**

### Step 2: Configure Database Settings
Fill in these fields:
- **Compartment:** Keep default (root)
- **Display name:** `RAG-VectorDB` (or any name you like)
- **Database name:** `RAGVECTORDB` (no spaces or special chars)
- **Workload type:** Select **"Transaction Processing"**
- **Deployment type:** Select **"Serverless"**
- **Always Free:** ✅ **Turn this ON** (make sure toggle is green)
- **Database version:** Select **"23ai"** (latest version)
- **OCPU count:** 1 (auto-set for Always Free)
- **Storage:** 20 GB (auto-set for Always Free)

### Step 3: Set Database Password
- **Password:** Create a strong password (remember this!)
  - Must have: uppercase, lowercase, number, special character
  - Example: `MyDB#Pass2024`
  - **Write this down!** You'll need it for the `.env` file

### Step 4: Network Access
- **Access Type:** Select **"Secure access from everywhere"**
  - This allows connections from your computer

### Step 5: License
- **License type:** Select **"License Included"**

### Step 6: Create Database
- Click **"Create Autonomous Database"**
- Wait 2-3 minutes for it to provision
- Status will change from **"PROVISIONING"** to **"AVAILABLE"** (green)

---

## Part 3: Get Database Connection Details

### Step 1: Find Your Database
1. In OCI Console, go to: **Oracle Database** → **Autonomous Database**
2. Click on your database name (`RAG-VectorDB`)

### Step 2: Get Connection String
1. Click **"Database connection"** button
2. Under **Connection Strings**, find the **"TNS Name"** section
3. Look for the one labeled **`<dbname>_low`** (e.g., `ragvectordb_low`)
4. Copy the **entire string** - it looks like:
   ```
   (description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=abc123_ragvectordb_low.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))
   ```

**Save this!** You'll paste this into your `.env` file.

---

## Part 4: Set Up OCI API Keys (for Generative AI)

### Step 1: Create API Key
1. In OCI Console, click your **profile icon** (top-right)
2. Click your username
3. On the left menu, click **"API keys"**
4. Click **"Add API key"**
5. Select **"Generate API key pair"**
6. Click **"Download private key"** - saves as `*.pem` file
7. Click **"Download public key"** (optional, for backup)
8. Click **"Add"**

### Step 2: Copy Configuration Details
After clicking "Add", you'll see a **Configuration File Preview**. It looks like:
```
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaa...
fingerprint=aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99
tenancy=ocid1.tenancy.oc1..aaaaaaaa...
region=us-ashburn-1
key_file=<path to your private keyfile>
```

**Copy these values:**
- `user` = Your User OCID
- `fingerprint` = Your API key fingerprint
- `tenancy` = Your Tenancy OCID
- `region` = Your home region

### Step 3: Move Your Private Key
1. Find the downloaded `.pem` file (probably in Downloads folder)
2. Move it to a safe location, example:
   ```
   C:\Users\YourName\.oci\oci_api_key.pem
   ```
3. Remember this path!

---

## Part 5: Get Your Compartment OCID

### Step 1: Find Compartment OCID
1. In OCI Console, click **hamburger menu** (☰)
2. Go to: **Identity & Security** → **Compartments**
3. You'll see a list - find the **root compartment** (usually named after your tenancy)
4. Click on it
5. Copy the **OCID** (starts with `ocid1.compartment.oc1..`)

**Note:** If you're using the root compartment, the compartment OCID might be the same as your tenancy OCID.

---

## Part 6: Fill in Your .env File

### Step 1: Open the .env File
1. In your project folder: `RAG-Chatbot-OCI-23ai`
2. Find the file named `.env`
3. Open it with Notepad or VS Code

### Step 2: Fill in OCI Section
Copy the values you collected from Part 4:

```ini
# ============================================================
# OCI CONFIGURATION
# ============================================================

# Your OCI User OCID (from API key setup, starts with ocid1.user.oc1..)
OCI_USER_OCID=ocid1.user.oc1..aaaaaaaa...

# Your OCI Tenancy OCID (from API key setup, starts with ocid1.tenancy.oc1..)
OCI_TENANCY_OCID=ocid1.tenancy.oc1..aaaaaaaa...

# Your OCI Compartment OCID (from Part 5, starts with ocid1.compartment.oc1..)
OCI_COMPARTMENT_OCID=ocid1.compartment.oc1..aaaaaaaa...

# Your home region (e.g., us-ashburn-1, us-phoenix-1, eu-frankfurt-1)
OCI_REGION=us-ashburn-1

# Full path to your private API key .pem file
# Windows example: C:\\Users\\YourName\\.oci\\oci_api_key.pem
# (Note: Use double backslashes \\ in Windows paths)
OCI_KEY_FILE=C:\\Users\\YourName\\.oci\\oci_api_key.pem

# The API key fingerprint (from API key setup, format: aa:bb:cc:...)
OCI_FINGERPRINT=aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99
```

### Step 3: Fill in Database Section
Use the values from Part 2 (password) and Part 3 (connection string):

```ini
# ============================================================
# ORACLE DATABASE CONFIGURATION
# ============================================================

# Database username - use 'ADMIN' (default admin user for Autonomous DB)
DB_USERNAME=ADMIN

# The password you created in Part 2, Step 3
DB_PASSWORD=MyDB#Pass2024

# The TNS connection string from Part 3, Step 2
# Paste the ENTIRE string between the quotes
DB_DSN=(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=abc123_ragvectordb_low.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))
```

### Step 4: Save the File
- Save and close the `.env` file
- **NEVER share this file** - it contains your credentials!

---

## Part 7: Run Your Project

### Step 1: First-Time Setup
Open Command Prompt in your project folder and run:
```batch
setup.bat
```
This will:
- Create virtual environment
- Install all Python packages
- Takes 2-3 minutes

### Step 2: Load Documents into Database
```batch
run_ingestion.bat
```
This will:
- Read all .txt files from the `data/` folder
- Create embeddings using OCI Generative AI
- Store them in your Oracle Vector Database
- Takes 30-60 seconds

### Step 3: Start the Chatbot
```batch
start_chatbot.bat
```
This will:
- Launch the Streamlit web app
- Open in your browser automatically
- Ask questions about your documents!

---

## Quick Reference: Where to Find Each Value

| **Value** | **Where to Find It** |
|-----------|---------------------|
| `OCI_USER_OCID` | Profile icon → Your username → User OCID (top of page) |
| `OCI_TENANCY_OCID` | Profile icon → Tenancy details → Tenancy OCID |
| `OCI_COMPARTMENT_OCID` | Menu → Identity → Compartments → Click compartment → Copy OCID |
| `OCI_REGION` | Shows in the top-right of OCI console (e.g., "US East (Ashburn)") |
| `OCI_KEY_FILE` | Path where you saved the downloaded `.pem` file |
| `OCI_FINGERPRINT` | Profile → API Keys → Listed next to your key |
| `DB_USERNAME` | Always `ADMIN` for Autonomous Database |
| `DB_PASSWORD` | The password you set when creating the database |
| `DB_DSN` | Your database page → Database Connection → TNS Name (copy the _low one) |

---

## Troubleshooting

### "Can't connect to database"
- ✅ Check your database is **AVAILABLE** (green) in OCI console
- ✅ Verify your `DB_PASSWORD` is correct
- ✅ Make sure you copied the **entire** TNS connection string (including parentheses)

### "OCI authentication failed"
- ✅ Verify your `.pem` file path is correct (use double backslashes `\\` on Windows)
- ✅ Check all OCIDs start with `ocid1.`
- ✅ Confirm your API key fingerprint matches what's shown in OCI console

### "Module not found" errors
- ✅ Run `setup.bat` again
- ✅ Make sure you see `(venv)` in your command prompt before running scripts

### "No documents found"
- ✅ Put `.txt` files in the `data/` folder
- ✅ Run `run_ingestion.bat` again

---

## Need Help?

1. **OCI Documentation:** https://docs.oracle.com/en-us/iaas/
2. **Oracle 23ai Docs:** https://docs.oracle.com/en/database/oracle/oracle-database/23/
3. **Check your OCI Free Tier limits:** Menu → Governance → Limits and Usage

---

**That's it! You're ready to build with RAG and Vector Search! 🚀**
