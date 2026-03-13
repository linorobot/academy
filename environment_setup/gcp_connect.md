# GCP VM Connection Guide

Now that your Cloud VM is running, you need a way to control it.

We offer three ways to connect:

| Option | Best For... | Description |
| :--- | :--- | :--- |
| **Option 1: Local Terminal** | **Robot Control** | The best experience for running commands. Supports `tmux`, `tmuxinator`, and shortcuts perfectly. |
| **Option 2: VS Code** | **Writing Code** | Best for editing files. Full file explorer, code completion, etc. |
| **Option 3: Quick Connect** | Quick fixes | Use the terminal in your browser. Fast, but hard to write code. |

---

## Phase 1: Global Setup (Required for Option 1 & 2)

To use Option 1 (Terminal) or Option 2 (VS Code), you must first create a digital "key card" (SSH Key) on your laptop.

**Step 1: Find your Username**
1.  Go to the [GCP Cloud Shell](https://ssh.cloud.google.com/cloudshell).
2.  Run the command `whoami`.
3.  **Write this down.** This is your Linux username (e.g., `john_doe`). You MUST use this exact name so you can access your files.

**Step 2: Generate an SSH Key**
Open **PowerShell** (Windows) or **Terminal** (Mac/Linux) on your laptop and run:

**Windows (PowerShell):**
```powershell
# Create the .ssh folder if it doesn't exist
mkdir $HOME\.ssh -ErrorAction SilentlyContinue

# Generate the key (Replace 'john_doe' with YOUR username)
ssh-keygen -t rsa -f $HOME\.ssh\gcp_key -C "john_doe"
```

**macOS / Linux:**
```bash
# Create folder
mkdir -p ~/.ssh

# Generate key (Replace 'john_doe' with YOUR username)
ssh-keygen -t rsa -f ~/.ssh/gcp_key -C "john_doe"
```
*(Press Enter twice to skip adding a password).*

**Step 3: Upload the Key to Google**
1.  Get the text of your public key:
    *   **Windows:** `Get-Content $HOME\.ssh\gcp_key.pub`
    *   **Mac/Linux:** `cat ~/.ssh/gcp_key.pub`
2.  Copy the **entire output** (starts with `ssh-rsa`... ends with your username).
3.  Go to [GCP Console -> Compute Engine -> VM Instances](https://console.cloud.google.com/compute/instances).
4.  Click **Your VM Instance Name** -> **Edit** -> Scroll down and find SSH keys -> **Add Item**.
5.  Paste your public key and click **Save**.

---

## Option 1: Local Terminal (Recommended for Robot Control)

**Why use this?**
Later in the course, we use `tmux` and `tmuxinator` to manage multiple robot programs. The Google Cloud Shell and VS Code terminal often capture standard shortcuts (like `Ctrl+W` or `Ctrl+B`) or have limited screen space, making these tools hard to use. A local terminal solves this.

**Instructions:**

1.  Find your VM's **External IP Address** in the GCP Console.
2.  Open **PowerShell** (Windows) or **Terminal** (Mac/Linux).
3.  Run the connection command (replace with your details):

    **Windows (PowerShell):**
    ```powershell
    ssh -i $HOME\.ssh\gcp_key -L 3000:localhost:3000 YOUR_USERNAME@YOUR_VM_IP
    ```

    **macOS / Linux:**
    ```bash
    ssh -i ~/.ssh/gcp_key -L 3000:localhost:3000 YOUR_USERNAME@YOUR_VM_IP
    ```

    *Tip: The `-L 3000:localhost:3000` part ensures you can see the simulator in your browser at `http://localhost:3000`.*

---

## Option 2: VS Code Remote (Recommended for Coding)

This setup allows you to use your local VS Code to edit files that are actually sitting on the Google Cloud Server.

**Step 1: Install Extension**
1.  Install **VS Code** on your laptop.
2.  Open VS Code -> Extensions (Square icon on left).
3.  Search for `Remote-SSH` (by Microsoft) and install it.

**Step 2: Connect**
1.  Find your VM's **External IP Address**.
2.  In VS Code, press `F1` (or Ctrl+Shift+P) and type: `Remote-SSH: Connect to Host...`.
3.  Select **Add New SSH Host...**
4.  Enter this command (replace with your details):
    ```bash
    ssh -i ~/.ssh/gcp_key YOUR_USERNAME@YOUR_VM_IP
    ```
5.  Select the configuration file to save to (usually the first option).
6.  Click **Connect**.
7.  Select **Linux** if asked.

You are now connected! Open Folder `/home/your_username/` to start coding.

---

## Option 3: Quick Connect (Browser Fallback)

If you cannot set up the options above, use this method.

1.  Open **Google Cloud Shell** (`>_` icon at [console.cloud.google.com](https://console.cloud.google.com)).
2.  Run the Magic Command:

```bash
export PROJECT_ID=$(gcloud projects list --format='value(projectId)') && export ZONE=$(gcloud compute instances list --project=$PROJECT_ID --format='value(zone)') && export VM_NAME=$(gcloud compute instances list --project=$PROJECT_ID --format='value(name)') && export PORT=3000 && echo "PROJECT_ID: $PROJECT_ID" && echo "ZONE: $ZONE" && echo "VM_NAME: $VM_NAME" && echo "PORT: $PORT"
```

3.  Run the SSH tunnel command output by the previous step:

```bash
gcloud compute ssh $VM_NAME \
  --zone=$ZONE \
  --tunnel-through-iap \
  --project=$PROJECT_ID \
  -- -L $PORT:localhost:$PORT
```

4.  Open `http://localhost:3000` in your browser.

---

## Next Steps

Now you have a computer and a connection!
Let's install the actual robot software.

👉 **Go to the [Docker Setup Guide](docker_setup.md)**


## Appendix: Manual Connection (For Multiple VMs)

If you have multiple VM instances, the auto-detection script in Option 1 might pick the wrong one. Use this manual method instead.

### Step 1: Open Google Cloud Shell

Go to [https://shell.cloud.google.com/](https://shell.cloud.google.com/) and open a Cloud Shell session.

### Step 2: List All Projects and Instances

Run this to see all available projects and instances:

```bash
PROJECT_ID=$(gcloud projects list --format='value(projectId)') && echo "PROJECT_ID: $PROJECT_ID" && gcloud compute instances list --project=$PROJECT_ID --format="table(name:label=VM_NAME,zone:label=ZONE)"
```

It will output something like:
```
PROJECT_ID: development-vm-402010
VM_NAME      ZONE
my-vm-1      asia-southeast1-b
my-vm-2      asia-southeast1-b
my-vm-3      us-central1-a
```

### Step 3: Set Environment Variables

Pick the instance you want to connect to and set the variables manually:

```bash
export PROJECT_ID="<YOUR_PROJECT_ID>"
export ZONE="<YOUR_ZONE>"
export VM_NAME="<YOUR_VM_NAME>"
export PORT=3000
```

### Step 4: SSH with Port Forwarding

```bash
gcloud compute ssh $VM_NAME \
  --zone=$ZONE \
  --tunnel-through-iap \
  --project=$PROJECT_ID \
  -- -L $PORT:localhost:$PORT
```

Once connected, your VM's port `3000` will be accessible at `localhost:3000` in your browser or local tools.

---

## Notes

### About `PORT`
- Port is always `3000` for this setup — no changes needed.
