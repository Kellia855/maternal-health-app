# maternal-health-app

This application helps expectant mothers track their pregnancy journey, receive health tips, set reminders, and find nearby hospitals. Follow these steps to set up and run the application successfully.

---

## Step 1: Clone the Repository

1. Open a terminal or command prompt.
2. Run the following command to clone the repository:
   ```sh
   git clone https://github.com/Kellia855/maternal-health-app.git
   ```
3. Navigate into the project folder:
   ```sh
   cd maternal-health-app
   ```

---

## Step 2: Set Up a Virtual Environment (Optional but Recommended)

A virtual environment ensures dependencies are managed properly.

1. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```

---

## Step 3: Install Dependencies

Install all required packages:
```sh
pip install -r requirements.txt
```

---

## Step 4: Set Up the Database

1. Ensure **MySQL** is installed and running.
2. Open MySQL and create a new database:
   ```sql
   CREATE DATABASE maternal_health;
   ```
3. Import the database schema (if provided):
   ```sh
   mysql -u root -p maternal_health < database.sql
   ```
4. Update the database credentials in `.env` (if applicable).

---

## Step 5: Run the Application

Start the program by running:
```sh
python main.py
```

---

## Step 6: Using the Application

1. **Register/Login** to create an account.
2. **Track Pregnancy** by viewing your progress and milestones.
3. **Set Reminders** for checkups, medications, and other health activities.
4. **View Health Tips** based on your pregnancy week.
5. **Find Nearby Hospitals** in your district.
6. **Update Profile** to change your details.
7. **Logout** when finished.

---

## Step 7: Git Workflow for Team Members

### Pull the Latest Changes
```sh
git pull origin main
```

### Create a New Branch
```sh
git checkout -b your-branch-name
```

### Make Changes and Commit
```sh
git add .
git commit -m "Your message here"
```

### Push to GitHub
```sh
git push origin your-branch-name
```

### Create a Pull Request
1. Go to GitHub.
2. Open a new **Pull Request (PR)** from your branch to `main`.
3. Request a review and merge once approved.

---

## Contributors
- Kellia Kamikazi(https://github.com/Kellia855)
- Divine Ikirezi(https://github.com/1kirezi)
- Sandrine Umugwaneza(https://github.com/sand02004)
- Michelle Anyika(https://github.com/Michelle-anyika)
- Rolande Tumugane(https://github.com/TRolande)
- Oriane Uwineza(https://github.com/uoriane)
- Teta Belyse Kalisa Yamwakate(https://github.com/kbelyse)

---

## Notes
- Ensure your MySQL server is running before starting the application.
- Always activate the virtual environment before running the program.
- If issues arise, check for missing dependencies with `pip list`.

This guide ensures you can set up and run the Maternal Health App smoothly. 
