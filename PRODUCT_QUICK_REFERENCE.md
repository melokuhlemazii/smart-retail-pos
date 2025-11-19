# Quick Reference Card - Product Management

## 🎯 Access Product Management

| Method | URL |
|---|---|
| Sidebar | Click "📦 Inventory" |
| Dashboard Button | Click "Manage Inventory" card |
| Direct URL | http://localhost:5000/manage_products |

---

## ➕ Add Product

```
1. Go to /manage_products
2. Click "Add New Product"
3. Fill form:
   - Code: UNIQUE identifier (2-20 chars)
   - Name: Product name (2-100 chars)
   - Category: Beverages, Bakery, Cleaning, etc.
   - Price: Amount in ZAR (e.g., 12.99)
   - Stock: Units in inventory (e.g., 25)
4. Click "Add Product"
```

---

## ✏️ Edit Product

```
1. Go to /manage_products
2. Find product in table
3. Click "✏️ Edit" button
4. Change any fields
5. Click "Update Product"
```

---

## 🗑️ Delete Product

```
1. Go to /manage_products
2. Find product in table
3. Click "Delete" button
4. Confirm deletion
5. Product removed from inventory
```

---

## 📊 Statistics Cards

| Card | Shows | Updates |
|---|---|---|
| 📦 Total Products | Count of all products | Automatically |
| ⚠️ Low Stock Items | Count with stock < 10 | Automatically |
| 💰 Stock Value | Total inventory value (ZAR) | Automatically |

---

## ⚠️ Low-Stock Alert

**Trigger**: Stock quantity < 10 units

**Display**:
- Red badge in product table
- Warning on edit form
- Counted in statistics

**Products Flagged**:
- Sunlight Dish Soap (9 units)
- Mandela Maize Meal (4 units)

---

## 🔒 Access Control

| Role | Can Access | Can Modify |
|---|---|---|
| Admin | ✅ Yes | ✅ Yes |
| Cashier | ❌ No | ❌ No |
| Public | ❌ No | ❌ No |

---

## 📦 Seed Products (Pre-Loaded)

```
1. Coca Cola 500ml       | Beverages | R12.99  | 25 units ✅
2. Brown Bread            | Bakery    | R16.50  | 12 units ✅
3. Sunlight Dish Soap     | Cleaning  | R34.99  | 9 units  ⚠️
4. Mandela Maize Meal 5kg | Pantry    | R72.00  | 4 units  ⚠️
5. Tastic Rice 2kg        | Pantry    | R48.99  | 15 units ✅
```

---

## 🔍 Form Fields

### Product Code
- Min: 2 chars
- Max: 20 chars
- Must be UNIQUE
- Example: COCOLA-500

### Name
- Min: 2 chars
- Max: 100 chars
- Example: Coca Cola 500ml

### Category
- Min: 2 chars
- Max: 50 chars
- Free text field
- Examples: Beverages, Bakery, Pantry

### Price (ZAR)
- Minimum: 0.01
- Currency: South African Rands
- Example: 12.99

### Stock Quantity
- Minimum: 0
- Integer only (no decimals)
- Example: 25

---

## ✅ Validation Errors

| Error | Cause | Fix |
|---|---|---|
| This field is required | Empty field | Fill in the field |
| This product code already exists | Duplicate code | Use unique code |
| Invalid price | Price ≤ 0 | Enter > 0.01 |
| Invalid stock | Negative stock | Enter ≥ 0 |
| Too short/long | Field length | Check min/max length |

---

## 🌍 Routes

| Route | Method | Purpose |
|---|---|---|
| `/manage_products` | GET | View all products |
| `/add_product` | GET | Show add form |
| `/add_product` | POST | Create product |
| `/edit_product/<id>` | GET | Show edit form |
| `/edit_product/<id>` | POST | Update product |
| `/delete_product/<id>` | POST | Delete product |
| `/product_stats` | GET | Get stats JSON |

---

## 💾 Database Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| id | Integer | ✅ | Auto-increment |
| product_code | String(20) | ✅ | UNIQUE |
| name | String(100) | ✅ | Product name |
| category | String(50) | ✅ | Category name |
| price | Float | ✅ | ZAR amount |
| stock_quantity | Integer | ✅ | Units in stock |
| date_created | DateTime | ✅ | Auto-set |
| date_updated | DateTime | ✅ | Auto-update |

---

## 🎯 Quick Actions

| Action | Click | Result |
|---|---|---|
| View Products | "Inventory" sidebar | Go to /manage_products |
| Add Product | "Add New Product" | Go to /add_product |
| Edit Product | "✏️ Edit" on row | Go to /edit_product/<id> |
| Delete Product | "🗑️ Delete" on row | Delete and redirect |
| Refresh Stats | Page reload | Auto-updates |

---

## 🔑 Test Logins

```
Admin:
Email: admin@example.com
Password: password

Cashier:
Email: cashier@example.com
Password: password
```

---

## 📱 Pagination

- **Per Page**: 10 products
- **Navigation**: Previous | Page 1 2 3 | Next
- **Display**: Shows 10 products per page
- **Auto**: Triggers at 11+ products

---

## 🔐 Security Tips

✅ Always use unique product codes  
✅ Validate price before adding  
✅ Check low-stock alerts  
✅ Logout when done  
✅ Don't share login credentials  
✅ Report errors immediately  

---

## 🆘 Troubleshooting

| Problem | Solution |
|---|---|
| "Access denied" | Login as admin |
| Code already exists | Use unique code |
| Product not found | Refresh page |
| Stats not updating | Reload page |
| Form won't submit | Check for errors |
| Can't see low stock | Check stock < 10 |

---

## 📞 Help Resources

| Guide | Purpose | Pages |
|---|---|---|
| PRODUCT_MANAGEMENT_GUIDE.md | Full documentation | 500+ |
| PRODUCT_MANAGEMENT_QUICKSTART.md | Quick start & testing | 350+ |
| PRODUCT_IMPLEMENTATION_SUMMARY.md | Implementation details | 300+ |
| SYSTEM_OVERVIEW.md | System architecture | 400+ |

---

## 🎉 Success Indicators

You'll know it's working when:

✅ Can view 5 seed products  
✅ Statistics cards display  
✅ Can add new product  
✅ Can edit product  
✅ Can delete product  
✅ Low-stock alerts show  
✅ Pagination works  
✅ Sidebar link active  
✅ Dashboard button works  

---

## 🚀 Next Steps

1. **Test** - Follow PRODUCT_MANAGEMENT_QUICKSTART.md
2. **Add** - Add more products
3. **Monitor** - Check low-stock items
4. **Explore** - Try all CRUD operations

---

**Quick Reference Card**  
**Last Updated**: November 19, 2025  
**Status**: ✅ READY TO USE

Print this card for quick reference!
