# 🧾 Receipt System - Quick Start Guide

## Overview
The Smart-Retail POS Receipt System provides professional, printable receipts for all completed sales transactions. Every receipt includes complete transaction details, itemized products, VAT calculations, and payment information.

---

## Features

### Receipt Contents
✅ **Header Section**
- Store name and branding
- Receipt type identification
- Receipt/Transaction number

✅ **Transaction Information**
- Date and time of transaction
- Cashier name
- Payment method (Cash/Card)

✅ **Itemized Products**
- Product name and code
- Quantity purchased
- Unit price
- Line total (quantity × price)

✅ **Financial Summary**
- Subtotal (before VAT)
- VAT amount (15%)
- Grand total (final amount due)

✅ **Footer**
- Thank you message
- VAT notice
- Complete timestamp

✅ **Functionality**
- Print directly from browser
- View transaction history
- Display detailed transaction stats

---

## How to Access Receipts

### Method 1: From Checkout
```
1. Complete POS sale (add items and checkout)
2. Select payment method
3. Click "Complete Sale"
4. Automatically redirected to receipt page
5. Click "🖨️ Print Receipt" to print
```

### Method 2: From Sales History
```
1. Go to Staff Dashboard
2. Click "Sales History"
3. Browse past transactions
4. Click on a transaction to view receipt
5. Print if needed
```

### Method 3: Direct URL Access
```
URL: /receipt/<transaction_id>

Example: 
http://localhost:5000/receipt/42

Note: Can only view own receipts (security feature)
```

---

## Receipt Data Structure

### Database Model
```
Transaction
├── ID: 42
├── Cashier: John Doe
├── Subtotal: R1000.00
├── VAT (15%): R150.00
├── Grand Total: R1150.00
├── Payment: Cash
├── Status: Completed
├── Date: 2024-01-15 14:30:45
└── Sales (items in transaction)
    ├── Sale 1: Coca-Cola 500ml × 2 @ R25.99 = R51.98
    ├── Sale 2: Sprite 1L × 1 @ R32.50 = R32.50
    └── Sale 3: Water Bottle 500ml × 5 @ R15.00 = R75.00
```

---

## Receipt Layout

### Visual Layout
```
╔════════════════════════════════════════╗
║      🛒 SMART-RETAIL POS              ║
║     Point of Sale System              ║
║    Receipt Transaction                ║
╠════════════════════════════════════════╣
║                                        ║
║ Date: 2024-01-15                       ║
║ Time: 14:30:45                         ║
║ Receipt #: 42                          ║
║                                        ║
║ Cashier: John Doe                      ║
║ Payment: 💵 Cash                       ║
║                                        ║
╠════════════════════════════════════════╣
║ Product         Qty  Price    Total   ║
║────────────────────────────────────────║
║ Coca-Cola 500ml   2  R25.99  R51.98   ║
║ SKU: COLA001                           ║
║                                        ║
║ Sprite 1L         1  R32.50  R32.50   ║
║ SKU: SPRITE001                        ║
║                                        ║
║ Water Bottle      5  R15.00  R75.00   ║
║ SKU: WATER001                         ║
║                                        ║
╠════════════════════════════════════════╣
║                                        ║
║ Subtotal:             R1000.00        ║
║ VAT (15%):            R150.00         ║
║                                        ║
║ GRAND TOTAL:          R1150.00        ║
║                                        ║
╠════════════════════════════════════════╣
║                                        ║
║   Thank you for your purchase!        ║
║   2024-01-15 14:30:45                 ║
║                                        ║
║  15% VAT included in price            ║
║                                        ║
╚════════════════════════════════════════╝

📋 TRANSACTION DETAILS:
├─ ID: 42
├─ Items: 3
├─ Total Units: 8
└─ Payment: Cash
```

---

## Printing Receipts

### Print Options

#### Option 1: Browser Print Dialog
```
1. Click "🖨️ Print Receipt" button
2. Select printer from system dialog
3. Adjust page settings if needed
4. Click "Print"
```

#### Option 2: Print to PDF
```
1. Click "🖨️ Print Receipt"
2. Select "Print to File" or "Save as PDF"
3. Choose destination folder
4. Click "Save"
```

#### Option 3: Thermal Printer (POS Setup)
```
Configure in browser:
1. Go to Print Dialog
2. Select thermal printer
3. Set paper size to 80mm (standard POS receipt)
4. Remove margins for compact printing
```

### Print Preview
- Receipt displays with optimized formatting
- Monospace font for alignment
- Compact layout for receipt paper
- All details clearly visible

---

## Receipt Management Features

### View Receipt
```python
Route: /receipt/<transaction_id>
Method: GET
Auth: Cashier role required
Access: Can only view own receipts

Template Variables:
- transaction: Transaction object
- sales: List of Sale objects
- user: Current logged-in user
```

### Receipt Validation
- ✅ Cashier ownership verification
- ✅ Transaction status validation
- ✅ Data integrity checks
- ✅ Timestamp recording

---

## Sales History

### Accessing Sales History
```
1. Login as cashier
2. Go to Staff Dashboard
3. Click "📊 Sales History"
4. View all your completed sales
5. Paginated: 10 transactions per page
```

### Sales History Features
- **Sorted by Date**: Newest first (descending)
- **Pagination**: Navigate through pages
- **Details**: Click transaction to view receipt
- **Timestamp**: Exact date and time recorded

### Sales History Route
```python
Route: /sales_history
Method: GET
Parameters: page=1 (optional)
Auth: Cashier role required
Display: 10 items per page
Order: Most recent first
```

---

## VAT Calculation Details

### VAT Formula
```
Subtotal = Sum of all (Product Price × Quantity)
VAT Amount = Subtotal × 0.15  (15% tax rate)
Grand Total = Subtotal + VAT Amount
```

### Example
```
Items in cart:
- Item 1: R100.00 × 2 = R200.00
- Item 2: R50.00 × 1 = R50.00
- Item 3: R150.00 × 1 = R150.00

Subtotal = R200.00 + R50.00 + R150.00 = R400.00
VAT (15%) = R400.00 × 0.15 = R60.00
Grand Total = R400.00 + R60.00 = R460.00
```

### VAT Compliance
- 15% VAT rate included in all receipts
- VAT amount clearly displayed
- Compliance with retail regulations
- Auditable transaction records

---

## API Endpoints

### Get Receipt
```
GET /receipt/<transaction_id>
Parameters:
  - transaction_id (int): Transaction ID

Response:
  - Renders receipt.html template
  - 404 if transaction not found
  - Redirect if not authorized
```

### View Sales History
```
GET /sales_history?page=1
Parameters:
  - page (int): Page number (optional, default=1)

Response:
  - Renders sales_history.html template
  - Paginated transactions
  - Most recent first
```

### Get Product Statistics
```
GET /product_stats
Response (JSON):
  {
    "total_products": 50,
    "low_stock_products": 5,
    "total_stock_value": 15000.00
  }
```

---

## Error Handling

### Common Errors & Solutions

#### Error: Receipt Not Found (404)
```
Cause: Invalid transaction ID
Solution: Use correct transaction ID from sales history
```

#### Error: You can only view your own receipts
```
Cause: Trying to access another cashier's receipt
Solution: Access only your own receipts via sales history
```

#### Error: Cashier access required
```
Cause: Logged in as admin or customer
Solution: Login with cashier credentials
```

#### Error: Insufficient stock
```
Cause: Item quantity exceeds available stock
Solution: Reduce quantity before checkout
```

---

## Receipt Templates & Customization

### Current Template: `receipt.html`

**Features:**
- Responsive design (mobile & desktop)
- Print-optimized styling
- Bootstrap grid layout
- Tailwind CSS classes
- Professional appearance

**Customization Options:**
```html
<!-- Modify store name -->
<p class="text-2xl font-black text-blue-600">🛒 YOUR STORE NAME</p>

<!-- Adjust VAT rate (default 15%) -->
<span>VAT (15%):</span>  <!-- Change percentage if needed -->

<!-- Add/remove footer text -->
<p class="text-xs text-gray-600 mb-2">Your custom message here</p>
```

---

## Integration Example

### Complete Sale to Receipt Flow
```python
# 1. User adds items to cart (session storage)
session['cart'] = [
    {'product_id': 1, 'quantity': 2, 'unit_price': 25.99},
    {'product_id': 2, 'quantity': 1, 'unit_price': 32.50}
]

# 2. User proceeds to checkout
# POST /checkout with payment_method

# 3. System creates transaction
transaction = Transaction(
    cashier_id=current_user.id,
    subtotal=84.48,
    vat_amount=12.67,
    grand_total=97.15,
    payment_method='cash',
    status='completed'
)
db.session.add(transaction)
db.session.flush()  # Get transaction ID

# 4. Create sale records for each item
for item in cart:
    sale = Sale(
        transaction_id=transaction.id,
        product_id=item['product_id'],
        quantity=item['quantity'],
        unit_price=item['unit_price'],
        line_total=item['unit_price'] * item['quantity']
    )
    db.session.add(sale)

# 5. Update product stock
product.stock_quantity -= item['quantity']

# 6. Commit all changes
db.session.commit()

# 7. Clear cart and redirect to receipt
session['cart'] = []
return redirect(url_for('main.receipt', transaction_id=transaction.id))

# 8. User views receipt
# GET /receipt/<transaction_id>
# Template displays transaction details and sales
```

---

## Receipt Data Persistence

### Database Storage
```
✅ Transaction records stored permanently
✅ All sales linked to transactions
✅ Receipt data never deleted (audit trail)
✅ Timestamp recorded for every transaction
✅ Cashier information associated with sale
```

### Data Relationships
```
Transaction (1) ←→ (Many) Sale
           ↓
        Cashier (User)
         ↓
     Product details available via Sale
```

---

## Security Features

### Receipt Access Control
- ✅ Cashier can only view own receipts
- ✅ Admin role cannot access POS receipts directly
- ✅ Session-based authentication required
- ✅ Transaction ownership validation

### Data Protection
- ✅ Prices stored with correct precision
- ✅ VAT calculations verified
- ✅ Stock deduction atomic operation
- ✅ No receipt modification possible

---

## Performance Optimization

### Receipt Loading
- Direct database query by transaction ID
- Eager loading of related sales
- Efficient SQL joins
- Fast HTML rendering

### Sales History
- Pagination: 10 items per page
- Ordered by date (database index friendly)
- Cached user lookups
- Optimized query selection

---

## Testing Checklist

- [ ] Create transaction with multiple items
- [ ] Receipt displays all correct details
- [ ] VAT calculated as 15% of subtotal
- [ ] Print functionality works
- [ ] Sales history shows transactions
- [ ] Cannot view other cashier's receipts
- [ ] Receipt data persists after logout/login
- [ ] Stock properly deducted
- [ ] Payment method correctly recorded
- [ ] Timestamps accurate

---

## Troubleshooting

### Receipt Not Displaying
```
Check:
1. Transaction ID is correct
2. Logged in as correct cashier
3. Transaction status is 'completed'
4. Database connection active
```

### Print Not Working
```
Check:
1. JavaScript enabled in browser
2. Pop-ups allowed for receipt.html
3. Printer configured correctly
4. Sufficient paper in printer
```

### Missing Receipt Data
```
Check:
1. Transaction was completed (not voided)
2. Sales records created in database
3. Product stock was reduced
4. No database rollback occurred
```

---

## Future Enhancements

Potential improvements for future versions:
- [ ] Email receipt to customer
- [ ] SMS receipt notification
- [ ] Receipt history search/filter
- [ ] Digital signature on receipts
- [ ] QR code for receipt verification
- [ ] Multi-language support
- [ ] Receipt template customization
- [ ] Refund receipt generation
- [ ] Daily/weekly/monthly reports
- [ ] Integration with accounting software

---

**Version**: 1.0
**Last Updated**: 2024
**Status**: Fully Implemented & Tested ✅
