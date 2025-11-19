# Product Management - Quick Start & Testing Guide

## 🚀 Quick Start (2 minutes)

### Step 1: Access Product Management
1. Login as admin: `admin@example.com` / `password`
2. Go to Admin Dashboard
3. Click **"Inventory"** in the sidebar OR click **"Manage Inventory"** button

### Step 2: View Seed Products
You'll see 5 sample products already loaded:
- Coca Cola 500ml (25 units)
- Brown Bread (12 units)
- Sunlight Dish Soap (9 units) ⚠️ LOW STOCK
- Mandela Maize Meal (4 units) ⚠️ LOW STOCK
- Tastic Rice (15 units)

### Step 3: Add a New Product
1. Click **"Add New Product"** button
2. Fill in the form:
   - Product Code: `WATER-500` (unique identifier)
   - Name: `Aqua Water Bottle 500ml`
   - Category: `Beverages`
   - Price: `8.99`
   - Stock: `50`
3. Click **"Add Product"**
4. ✅ Product added! See success message

### Step 4: Edit a Product
1. Find a product in the list
2. Click **"Edit"** button
3. Change any field (e.g., increase stock from 9 to 20)
4. Click **"Update Product"**
5. ✅ Product updated!

### Step 5: Delete a Product
1. Find a product in the list
2. Click **"Delete"** button
3. Confirm deletion
4. ✅ Product removed!

---

## 🧪 Testing Scenarios

### Scenario 1: View Statistics
**Expected**: Statistics cards show real-time counts
```
Test:
  1. Go to /manage_products
  2. Check statistics cards
  
Expected Results:
  ✅ Total Products = 5 (or more if you added)
  ✅ Low Stock Items = 2 (SOAP-750, MAIZE-5KG)
  ✅ Total Stock Value = R256.83 (or new total)
```

### Scenario 2: Add Product with Validation
**Expected**: Form validates all fields
```
Test:
  1. Click "Add New Product"
  2. Try to submit empty form
  
Expected Results:
  ✅ Error: "This field is required" for each empty field
  ✅ Cannot submit invalid data
  ✅ Price validates > 0.01
  ✅ Stock validates >= 0
```

### Scenario 3: Unique Product Code
**Expected**: Cannot create duplicate product codes
```
Test:
  1. Click "Add New Product"
  2. Code: COCOLA-500 (already exists)
  3. Fill other fields and submit
  
Expected Results:
  ✅ Error: "This product code already exists."
  ✅ Product not created
  ✅ Returned to form
```

### Scenario 4: Low Stock Alert
**Expected**: Products with < 10 units show alert
```
Test:
  1. Go to /manage_products
  2. Look at product table
  
Expected Results:
  ✅ SOAP-750 shows red badge: "⚠️ LOW STOCK"
  ✅ MAIZE-5KG shows red badge: "⚠️ LOW STOCK"
  ✅ Others show normal stock count
  ✅ Edit form shows warning for low stock items
```

### Scenario 5: Edit and Update Stock
**Expected**: Can increase stock to above 10 units
```
Test:
  1. Find SOAP-750 (9 units, low stock)
  2. Click "Edit"
  3. Change stock to 25
  4. Click "Update Product"
  5. Go back to list
  
Expected Results:
  ✅ Stock updated to 25
  ✅ Low stock alert removed
  ✅ Statistics updated
  ✅ Success message shown
```

### Scenario 6: Delete Product
**Expected**: Product removed from system
```
Test:
  1. Find any product
  2. Click "Delete"
  3. Confirm deletion
  
Expected Results:
  ✅ Product removed from table
  ✅ Statistics updated (total_products decreased)
  ✅ Success message shown
  ✅ Page refreshed with new list
```

### Scenario 7: Pagination
**Expected**: Handles > 10 products with pagination
```
Test:
  1. Add 10+ products (click "Add New Product" multiple times)
  2. Watch pagination
  
Expected Results:
  ✅ First page shows 10 products
  ✅ "Next" button appears
  ✅ Can navigate between pages
  ✅ Page counter updates
```

### Scenario 8: Security - Cashier Blocked
**Expected**: Cashier cannot access product management
```
Test:
  1. Logout
  2. Login as cashier: `cashier@example.com` / `password`
  3. Try to visit /manage_products directly
  
Expected Results:
  ✅ Redirect to login page
  ✅ Error message: "Access denied: Administrator access required."
  ✅ Sidebar doesn't show "Inventory" link
```

---

## 📊 Data Validation Rules

### Product Code
- **Min Length**: 2 characters
- **Max Length**: 20 characters
- **Must be Unique**: No duplicates allowed
- **Example**: `COCOLA-500`, `BREAD-01`, `SOAP-750`

### Product Name
- **Min Length**: 2 characters
- **Max Length**: 100 characters
- **Required**: Cannot be empty
- **Example**: `Coca Cola 500ml`, `Brown Bread`

### Category
- **Min Length**: 2 characters
- **Max Length**: 50 characters
- **Required**: Cannot be empty
- **Example**: `Beverages`, `Bakery`, `Cleaning`, `Pantry`

### Price (ZAR)
- **Minimum**: 0.01
- **Required**: Cannot be empty
- **Currency**: South African Rands
- **Example**: `12.99`, `34.99`, `72.00`

### Stock Quantity
- **Minimum**: 0
- **Integer Only**: No decimals
- **Required**: Cannot be empty
- **Alert Threshold**: < 10 = Low Stock
- **Example**: `25`, `9`, `0`

---

## 🔒 Security Features

### Access Control
✅ Only admins can access `/manage_products`  
✅ Cashiers automatically redirected with error message  
✅ Login required for all routes  

### Data Protection
✅ SQL injection prevented (SQLAlchemy ORM)  
✅ Input validation on all fields  
✅ Unique constraint on product codes  
✅ No sensitive data exposed in URLs  

### User Feedback
✅ Success messages on create/update/delete  
✅ Error messages for validation failures  
✅ Flash messages auto-dismiss  
✅ Confirmation dialog on delete  

---

## 📱 Navigation Paths

### From Admin Dashboard
```
Dashboard → "Manage Inventory" button → /manage_products
```

### From Sidebar
```
Sidebar → "Inventory" link → /manage_products
```

### Direct URL
```
http://localhost:5000/manage_products
```

---

## 🆘 Troubleshooting

### "Access denied" message
**Problem**: You're logged in as cashier
**Solution**: Logout and login as admin

### "This product code already exists"
**Problem**: Product code is duplicate
**Solution**: Use a unique product code (e.g., add timestamp: BREAD-01, BREAD-02)

### Statistics not updating
**Problem**: JavaScript not loading stats
**Solution**: Refresh page with F5 or Ctrl+Shift+R

### Low stock alert not showing
**Problem**: Stock might be >= 10
**Solution**: Edit product to have stock < 10

### Cannot add product
**Problem**: Validation error
**Solution**: Check all required fields are filled and prices > 0

### "404 Product Not Found"
**Problem**: Product already deleted
**Solution**: Refresh page to see current list

---

## 🎯 Testing Checklist

### Create Test
- [ ] Add "Test Pepsi 500ml" (Beverages, R13.99, 30 units)
- [ ] Verify success message
- [ ] Verify product appears in list
- [ ] Verify statistics updated

### Read Test
- [ ] View all 5+ seed products
- [ ] Check statistics cards accurate
- [ ] Verify low stock alerts visible
- [ ] Test pagination if > 10 products

### Update Test
- [ ] Edit "Test Pepsi" to "Pepsi 500ml"
- [ ] Change category to "Soft Drinks"
- [ ] Change price to R13.50
- [ ] Reduce stock to 5 (low stock alert)
- [ ] Verify updates saved

### Delete Test
- [ ] Delete "Pepsi 500ml"
- [ ] Verify success message
- [ ] Verify product removed from list
- [ ] Verify statistics updated

### Security Test
- [ ] Logout
- [ ] Login as cashier
- [ ] Try to access /manage_products
- [ ] Verify redirect to login
- [ ] Verify error message shown

---

## 📊 Statistics Explanation

### Total Products
Shows count of all products in inventory
- Increases when you add products
- Decreases when you delete products

### Low Stock Items
Shows count of products with stock < 10 units
- SOAP-750: 9 units ✓
- MAIZE-5KG: 4 units ✓
- Other products: >= 10 units

### Total Stock Value
Calculates total value of all inventory
- Formula: SUM(price × stock_quantity)
- Example: COCOLA-500 = R12.99 × 25 = R324.75
- All values combined = Total Stock Value

---

## 🎓 Product Categories Guide

You can use any category. Here are common ones:

| Category | Examples |
|---|---|
| Beverages | Soft drinks, water, juice, alcohol |
| Bakery | Bread, cakes, pastries, flour |
| Cleaning | Detergents, soaps, disinfectants, bleach |
| Pantry | Grains, rice, maize meal, sugar, salt |
| Dairy | Milk, cheese, yogurt, butter |
| Fresh | Fruits, vegetables, meat, fish |
| Personal Care | Shampoo, toothpaste, deodorant, soap |
| Frozen | Ice cream, frozen meals, frozen vegetables |

---

## 🔗 Quick Links

| Link | URL |
|---|---|
| Manage Products | http://localhost:5000/manage_products |
| Add Product | http://localhost:5000/add_product |
| Product Stats | http://localhost:5000/product_stats |
| Admin Dashboard | http://localhost:5000/admin_dashboard |
| Logout | http://localhost:5000/logout |

---

## ✅ Success Indicators

You'll know it's working when you see:

1. ✅ 5 seed products in the list
2. ✅ Statistics cards show values
3. ✅ Low stock warnings visible
4. ✅ Can add new products
5. ✅ Can edit products
6. ✅ Can delete products
7. ✅ Flash messages on success
8. ✅ Errors prevent bad data
9. ✅ Sidebar link visible
10. ✅ Dashboard card functional

---

## 📞 Support

If something isn't working:

1. **Check Server**: Is Flask running at http://127.0.0.1:5000?
2. **Refresh Page**: Try Ctrl+Shift+R to clear cache
3. **Check Login**: Are you logged in as admin?
4. **Check Browser Console**: F12 → Console tab for JavaScript errors
5. **Restart App**: Stop Flask and run `python run.py` again
6. **Reinit DB**: Run `python init_db.py` and `python seed_products.py`

---

**Last Updated**: November 19, 2025  
**Status**: ✅ READY TO TEST  
**Seed Products**: 5  
**Test Scenarios**: 8
