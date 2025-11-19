# User Management System - Quick Start & Testing

## 🚀 Quick Start

### Access User Management
1. **Login as Administrator**
   - Go to: http://127.0.0.1:5000
   - Login with your admin account credentials

2. **From Admin Dashboard**, click one of:
   - **"Manage Users"** button in Quick Actions
   - **"Manage Cashiers"** in sidebar

---

## 📋 Features At A Glance

### View All Users
**URL**: `http://127.0.0.1:5000/manage_users`

Shows:
- Total user count
- Total admin count
- Total cashier count
- Complete user list (paginated)
- Edit/Delete buttons per user

### Add New User
**URL**: `http://127.0.0.1:5000/add_user`

Create new user with:
- Full name
- Email address
- Password (min 6 characters)
- Role (Administrator / Cashier)

### Edit User
**URL**: `http://127.0.0.1:5000/edit_user/<user_id>`

Modify:
- User name
- Email address
- Role
- Password (optional)

### Delete User
**Action**: Click "Delete" button on user row

Removes user account (with confirmation)

---

## 🧪 Testing Scenarios

### Scenario 1: Add a Cashier
```
1. Click "Manage Users"
2. Click "Add New User" button
3. Enter:
   - Name: "John Doe"
   - Email: "john@example.com"
   - Password: "secure123"
   - Role: Cashier
4. Click "Add User"
5. ✅ Success message displays
6. John Doe appears in user list
```

### Scenario 2: Add an Administrator
```
1. Click "Manage Users"
2. Click "Add New User" button
3. Enter:
   - Name: "Jane Admin"
   - Email: "jane@example.com"
   - Password: "secure456"
   - Role: Administrator
4. Click "Add User"
5. ✅ Jane Admin appears with Administrator badge
6. Administrator count increases
```

### Scenario 3: Edit a User
```
1. In manage_users page, click "Edit" on a user
2. Modify:
   - Name: "John Smith" (changed from John Doe)
   - Role: Administrator (changed from Cashier)
3. Leave password blank (keep current)
4. Click "Update User"
5. ✅ User updated, returns to user list
6. Changes reflected immediately
```

### Scenario 4: Change User Password
```
1. Click "Edit" on any user
2. In "Change Password" section, enter:
   - New Password: "newpass789"
   - Confirm Password: "newpass789"
3. Click "Update User"
4. ✅ Password changed
5. User can login with new password
```

### Scenario 5: Delete a User
```
1. In user list, click "Delete" on a user
2. Confirm the deletion dialog
3. ✅ User removed from list
4. Success message displays
5. Total user count decreases
```

### Scenario 6: Security - Cannot Delete Own Account
```
1. As admin, try to delete your own account
2. "Delete" button is disabled (shows "You (Owner)")
3. ✅ Cannot self-delete
```

### Scenario 7: Access Control - Cashier Blocked
```
1. Login as Cashier
2. Try to visit: http://127.0.0.1:5000/manage_users
3. ❌ Redirected to login page
4. Error message: "Access denied: Administrator access required."
```

---

## 📊 Statistics

The system tracks:
- **Total Users**: All accounts (admins + cashiers)
- **Administrators**: Accounts with 'admin' role
- **Cashiers**: Accounts with 'staff' role

Stats update in real-time as users are added/deleted.

---

## ✅ Validation Rules

### Email
- ✅ Must be valid format (user@example.com)
- ✅ Must be unique (no duplicates)
- ✅ Cannot leave blank

### Password
- ✅ Minimum 6 characters
- ✅ Must confirm match
- ✅ Automatically hashed with bcrypt
- ✅ Cannot leave blank on add

### Name
- ✅ Minimum 2 characters
- ✅ Maximum 20 characters
- ✅ Cannot leave blank

### Role
- ✅ Must select Administrator or Cashier
- ✅ Cannot leave blank

---

## 🔒 Security Features

✅ **Password Hashing**: bcrypt encryption
✅ **Email Uniqueness**: No duplicate registrations
✅ **Admin-Only Access**: Cashiers completely blocked
✅ **Self-Delete Prevention**: Cannot delete own account
✅ **Confirmation Required**: Delete action requires confirmation
✅ **Session Required**: Must be logged in
✅ **Role Validation**: Server-side role verification

---

## 📱 User Interface

### Manage Users Page
```
[Total Users: 5] [Administrators: 2] [Cashiers: 3]

[➕ Add New User]

┌─────────────────────────────────────────────────┐
│ Name     │ Email    │ Role    │ Created  │ Actions │
├─────────────────────────────────────────────────┤
│ John     │ john@... │ Cashier │ Nov 19   │ [Edit] [Delete] │
│ Jane     │ jane@... │ Admin   │ Nov 19   │ [Edit] You (Owner) │
│ Bob      │ bob@...  │ Cashier │ Nov 19   │ [Edit] [Delete] │
└─────────────────────────────────────────────────┘

[< Previous] [1] [2] [Next >]
```

### Add/Edit Form
```
Full Name: [________________________]
Email:     [________________________]
Role:      [Administrator ▼]
Password:  [________________________]
Confirm:   [________________________]

[Add User] [Cancel]
```

---

## 📍 URLs Reference

| Action | URL | Method |
|--------|-----|--------|
| View Users | `/manage_users` | GET |
| Add User Form | `/add_user` | GET |
| Submit Add | `/add_user` | POST |
| Edit User Form | `/edit_user/1` | GET |
| Submit Edit | `/edit_user/1` | POST |
| Delete User | `/delete_user/1` | POST |
| Get Stats | `/user_stats` | GET (JSON) |

---

## 🐛 Troubleshooting

### Issue: "Email already registered"
**Solution**: Use a unique email address not already in the system

### Issue: "Passwords must match"
**Solution**: Ensure password and confirm password are identical

### Issue: Cannot access user management
**Solution**: Make sure you're logged in as Administrator, not Cashier

### Issue: Delete button not working
**Solution**: Cannot delete your own account. Try deleting a different user

---

## 📈 Statistics API

Get user statistics as JSON:

```bash
curl http://127.0.0.1:5000/user_stats
```

Response:
```json
{
  "total_users": 5,
  "total_admins": 2,
  "total_cashiers": 3
}
```

---

## 💾 Data Persistence

All user changes are immediately saved to the database:
- `site.db` (SQLite)

No need to manually save or restart the application.

---

## 🎯 Next Steps

After implementing user management:
1. Add more users for testing
2. Try different roles (Administrator/Cashier)
3. Test editing and password changes
4. Verify access control
5. Test with Cashier account (should be blocked)

---

**Ready to test!** 🚀

Start at: http://127.0.0.1:5000

Login → Admin Dashboard → Manage Users
