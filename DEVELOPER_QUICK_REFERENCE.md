# 🎯 Smart-Retail POS System - Developer Quick Reference

## Quick Navigation

### Essential Files
| File | Purpose | Lines |
|------|---------|-------|
| `run.py` | Application entry point | 10 |
| `app/__init__.py` | Flask initialization | 45 |
| `app/models.py` | Database models | 175 |
| `app/forms.py` | Form definitions | 250+ |
| `app/main/routes.py` | Main routes (POS) | 450+ |
| `app/auth/routes.py` | Auth routes | 100+ |
| `config.py` | Configuration | 50+ |
| `init_db.py` | Database setup | 50+ |

---

## Running the Application

### Start Server
```bash
# Activate environment
.\venv\Scripts\Activate.ps1

# Run application
python run.py

# Access at http://localhost:5000
```

### Initialize Database
```bash
# Create fresh database
python init_db.py

# Seed sample data (optional)
python seed_products.py
```

---

## Database Models Quick Reference

### User Model
```python
User(
    id, name, email, password_hash,
    role='admin'|'staff', date_created
)
```

### Product Model
```python
Product(
    id, product_code, name, category,
    price, stock_quantity, 
    date_created, date_updated
)
```

### Transaction Model
```python
Transaction(
    id, cashier_id, subtotal, vat_amount,
    grand_total, payment_method,
    status, date_created
)
```

### Sale Model
```python
Sale(
    id, transaction_id, product_id,
    quantity, unit_price, line_total,
    date_created
)
```

---

## Key Routes Quick Reference

### Auth Routes
```
POST   /auth/register      → Register new user
POST   /auth/login         → Login user
GET    /auth/logout        → Logout user
```

### Admin Routes
```
GET    /manage_users       → List users
POST   /add_user           → Create user
POST   /edit_user/<id>     → Update user
POST   /delete_user/<id>   → Delete user
GET    /manage_products    → List products
POST   /add_product        → Create product
POST   /edit_product/<id>  → Update product
POST   /delete_product/<id> → Delete product
GET    /user_stats         → User statistics (JSON)
GET    /product_stats      → Product statistics (JSON)
```

### Cashier Routes
```
GET    /pos                → POS interface
POST   /add_to_cart/<id>   → Add item
POST   /update_cart/<id>   → Update quantity
POST   /remove_from_cart/<id> → Remove item
POST   /clear_cart         → Clear cart
POST   /checkout           → Checkout
GET    /receipt/<id>       → View receipt
GET    /sales_history      → View history
```

---

## Common Code Patterns

### Login Required
```python
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
```

### Role Check
```python
if current_user.role != 'admin':
    flash('Access denied', 'danger')
    return redirect(url_for('auth.login'))
```

### Form Submission
```python
if form.validate_on_submit():
    # Process form
    db.session.add(obj)
    db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('main.list'))
```

### Error Handling
```python
try:
    # Database operations
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash(f'Error: {str(e)}', 'danger')
```

---

## Template Structure

### Base Template (`base.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% include 'nav.html' %}
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <!-- Display messages -->
        {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
</body>
</html>
```

### Form Rendering
```html
<form method="POST">
    {{ form.hidden_tag() }}
    {% if form.errors %}
        <!-- Display errors -->
    {% endif %}
    {{ form.submit() }}
</form>
```

### Loops
```html
{% for item in items %}
    <tr>
        <td>{{ item.name }}</td>
        <td>R {{ "%.2f"|format(item.price) }}</td>
    </tr>
{% endfor %}
```

---

## Console Commands

### Database Operations
```bash
# Create database
python init_db.py

# Seed data
python seed_products.py

# Query with SQLite
sqlite3 instance/site.db "SELECT * FROM user;"
```

### Check Database Tables
```bash
sqlite3 instance/site.db ".tables"
sqlite3 instance/site.db ".schema user"
```

### Run Flask Shell
```bash
flask shell

# Inside shell
>>> from app import db
>>> from app.models import User, Product
>>> User.query.all()
>>> Product.query.filter_by(category='Beverages').all()
```

---

## Frontend Quick Reference

### Tailwind Classes (Common)
```
# Colors
bg-blue-600       text-white       text-gray-600

# Sizing
p-6               m-4              w-full            h-screen

# Display
flex              grid             hidden            block

# Responsive
sm: md: lg: xl:   (prefixes for breakpoints)

# States
hover: focus: active: disabled:
```

### Form Handling
```html
<!-- Text Input -->
{{ form.name(class="form-control") }}

<!-- Select -->
{{ form.role() }}

<!-- Textarea -->
{{ form.description(rows=4) }}

<!-- Submit -->
{{ form.submit(class="btn btn-primary") }}

<!-- Errors -->
{% if form.email.errors %}
    <span class="error">{{ form.email.errors[0] }}</span>
{% endif %}
```

---

## Common Troubleshooting

### Issue: Module not found
```bash
# Solution
pip install -r requirements.txt
```

### Issue: Database locked
```bash
# Solution
rm instance/site.db
python init_db.py
```

### Issue: Port 5000 in use
```python
# In run.py
app.run(debug=True, port=5001)
```

### Issue: Template not found
```
Check:
- File exists in app/templates/
- Correct filename spelling
- Template inheritance correct
```

### Issue: Import error
```
Check:
- Virtual environment activated
- Package installed (pip install)
- Correct import path
```

---

## Development Workflow

### 1. Make Code Changes
```python
# Edit file
# Example: app/main/routes.py
```

### 2. Test Changes
```bash
# Application auto-reloads in debug mode
# Just refresh browser
```

### 3. Test Database
```bash
# Verify data
sqlite3 instance/site.db "SELECT * FROM user;"
```

### 4. Commit Changes
```bash
git add .
git commit -m "Description of changes"
```

---

## Performance Tips

### Query Optimization
```python
# Good: Load related objects
users = User.query.with_entities(User.name, User.email).all()

# Bad: N+1 queries
for user in users:
    print(user.transactions)  # New query each time
```

### Caching
```python
# Cache expensive queries
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300)
def get_stats():
    return expensive_query()
```

### Pagination
```python
# Use pagination for large datasets
page = request.args.get('page', 1, type=int)
items = Item.query.paginate(page=page, per_page=10)
```

---

## Security Checklist

Before deployment:
- [ ] Change SECRET_KEY in .env
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/SSL
- [ ] Use strong database password
- [ ] Disable debug mode
- [ ] Set up logging
- [ ] Configure CORS if needed
- [ ] Setup backup procedures
- [ ] Test authentication thoroughly
- [ ] Validate all inputs

---

## File Structure Quick Map

```
possystem/
├── app/
│   ├── __init__.py          # Flask init
│   ├── models.py            # Database models
│   ├── forms.py             # Form classes
│   ├── utils.py             # Helper functions
│   ├── main/                # POS blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # 450+ lines
│   ├── auth/                # Auth blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── pos.html
│   │   ├── receipt.html
│   │   └── [15+ more]
│   └── static/              # CSS, JS, images
├── run.py                   # Entry point
├── config.py                # Configuration
├── init_db.py               # Database setup
├── seed_products.py         # Sample data
├── requirements.txt         # Dependencies
└── .env                     # Environment vars
```

---

## Git Workflow

### Initial Setup
```bash
git init
git add .
git commit -m "Initial POS system commit"
```

### Regular Commits
```bash
# Check status
git status

# Stage changes
git add <file>
# or
git add .

# Commit
git commit -m "Descriptive message"
```

### Branches (Optional)
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Test
# Commit

# Merge back
git checkout main
git merge feature/new-feature
```

---

## Environment Variables (.env)

```env
# Required
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///site.db
FLASK_ENV=development

# Optional
FLASK_DEBUG=True
SERVER_NAME=localhost:5000
LOG_LEVEL=INFO
```

---

## Testing Template

```python
# Example test
def test_add_product():
    # Setup
    admin = User(email='admin@test.com', role='admin')
    db.session.add(admin)
    db.session.commit()
    
    # Action
    product = Product(
        product_code='TEST001',
        name='Test Product',
        price=10.00
    )
    db.session.add(product)
    db.session.commit()
    
    # Assert
    assert Product.query.count() == 1
    assert product.name == 'Test Product'
```

---

## Documentation Map

| Document | Purpose | Length |
|----------|---------|--------|
| POS_SYSTEM_COMPLETE_GUIDE.md | Full system docs | 800+ lines |
| RECEIPT_SYSTEM_GUIDE.md | Receipt details | 600+ lines |
| IMPLEMENTATION_VERIFICATION_CHECKLIST.md | Verification | 500+ lines |
| POS_SYSTEM_FINAL_SUMMARY.md | Project summary | 400+ lines |
| Developer Quick Reference | This file | 400 lines |

---

## Quick Links & References

### Official Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Tailwind CSS: https://tailwindcss.com/
- Jinja2: https://jinja.palletsprojects.com/

### Python Best Practices
- PEP 8: https://pep8.org/
- Clean Code: Code readability
- SOLID: Design principles

### Tools & Extensions
- VS Code: Code editor
- Git: Version control
- SQLite: Database viewer

---

## Support & Help

**Problem?**
1. Check the comprehensive guides
2. Review code comments
3. Check error messages
4. Review database with SQLite
5. Check application logs

**Guides Available:**
- POS_SYSTEM_COMPLETE_GUIDE.md
- RECEIPT_SYSTEM_GUIDE.md
- IMPLEMENTATION_VERIFICATION_CHECKLIST.md
- This quick reference

---

## Key Metrics

### Code Statistics
- **Models**: 4
- **Routes**: 20+
- **Templates**: 15+
- **Forms**: 8+
- **Functions**: 50+
- **Lines of Code**: 5000+

### Features
- User Management ✅
- Product Management ✅
- POS System ✅
- Receipt Generation ✅
- Sales History ✅
- Statistics ✅

### Performance
- Pagination: 10 items/page
- Database: SQLite (local)
- Response Time: < 500ms
- Load Time: < 1s

---

## Last But Not Least

### Remember:
- Always test before deploying
- Backup database regularly
- Keep dependencies updated
- Monitor application logs
- Secure your .env file
- Use strong passwords
- Document your changes
- Comment complex logic
- Follow naming conventions
- Handle errors gracefully

---

**Smart-Retail POS System**
**Developer Quick Reference v1.0**
**Ready to Code! 🚀**

---

For comprehensive information, see:
- POS_SYSTEM_COMPLETE_GUIDE.md (Full documentation)
- RECEIPT_SYSTEM_GUIDE.md (Receipt features)
- IMPLEMENTATION_VERIFICATION_CHECKLIST.md (Testing)
