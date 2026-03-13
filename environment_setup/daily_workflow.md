# Daily Development Workflow ⚡

> **Prerequisite:** You must have completed the [Environment Setup](README.md) before using this guide.

Use this guide every time you want to start working on the robot exercises.

---

## 1. Start Your Cloud VM (GCP Users Only)

> **Skip this if acts as a local Ubuntu machine.**

Your cloud computer costs money while it is running. Only start it when you are ready to work.

**Method A: Visual Console**
1.  Go to [GCP Compute Instances](https://console.cloud.google.com/compute/instances).
2.  Check the box next to your VM instance.
3.  Click **Start / Resume** (Play icon) at the top.
4.  **Wait** for the green checkmark and copy the **External IP** (it often changes!).

**Method B: Command Line**
(If you have `gcloud` configured locally)
```bash
gcloud compute instances start YOUR_VM_NAME --zone=YOUR_ZONE
```

---

## 2. Connect to the Machine

**Option 1: Local Terminal (Recommended for Running Robot)**
Use this for `tmuxinator` commands and controlling the robot.
```bash
# Replace with your actual username and IP
ssh -i ~/.ssh/gcp_key -L 3000:localhost:3000 YOUR_USERNAME@YOUR_VM_IP
```

**Option 2: VS Code (Recommended for Coding)**
Use this for writing code.
1.  Open VS Code.
2.  `F1` -> `Remote-SSH: Connect to Host...`.
3.  (If IP changed) `Remote-SSH: Open Configuration File...` and update the `HostName` with the new IP.
4.  Connect.

---

## 3. Start the Simulation

1.  **Navigate to the docker folder:**
    ```bash
    cd ~/linorobot2/docker
    ```

2.  **Choose your mode:**

    | Mode | Command | Best For... |
    | :--- | :--- | :--- |
    | **Quick Launch** | `tmuxinator start sim` | Verify the setup. Automatically launches the robot & world. |
    | **Development** | `tmuxinator start dev` | **Class Exercises.** Givens you empty terminals to run commands yourself. |

3.  **View the Simulation:**
    Open [http://localhost:3000](http://localhost:3000) in your web browser.

---

## 4. Stopping Your Session (Critical) 🛑

When you are done, you **must** shut everything down to avoid losing work or paying for idle cloud time.

**Step 1: Stop the Simulation**
1.  In your terminal, press `Ctrl+B`.
2.  Type `:kill-session` and press `Enter`.
    *Alternatively, run `tmuxinator stop dev` (or `sim`).*

**Step 2: Stop the Cloud VM**
**⚠️ YOU MUST DO THIS TO STOP BILLING.**

1.  Go to [GCP Compute Instances](https://console.cloud.google.com/compute/instances).
2.  Select your VM.
3.  Click **Stop**.

*(Or use the command line: `gcloud compute instances stop YOUR_VM_NAME`)*
