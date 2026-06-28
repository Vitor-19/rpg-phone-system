# RPG Phone System 📱

A Discord bot for immersive RPG communication, simulating an in-game phone system for players and game masters.

It allows GMs to assign phones to players, send messages between characters, and manage in-game communications through private channels.

---

## ✨ Features

- Role-based phone system (players & GMs)
- Automatic setup command (roles + private log channel)
- Private message logging visible only to GMs
- In-game phone messaging system
- GM-controlled message delivery
- Slash command interface

---

## 🧠 Commands

### `/setup_phone_system`
Initializes the RPG phone system in the server.

- Creates required roles automatically
- Creates private GM-only log channel
- Grants GM role to the command executor

---

### `/give_phone`
Gives a phone to a player.

Requires: GM role

---

### `/rem_phone`
Removes a phone from a player.

Requires: GM role

---

### `/phone_call`
Sends an in-game message through the phone system.

Requires: GM role

---

### `/phone_res`
Responds to a player's message via DM.

Requires: GM role

---

## ⚙️ Setup

```bash
pip install -r requirements.txt