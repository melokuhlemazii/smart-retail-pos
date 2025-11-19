from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flask_login import login_required, current_user
from app import db, bcrypt
from app.models import User, Product, Transaction, Sale
from app.forms import AddUserForm, EditUserForm, AddProductForm, EditProductForm, SearchProductForm, AddToCartForm, CheckoutForm
from app.main import bp
from datetime import datetime

@bp.route('/')
def landing():
    return render_template("index.html")

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    total_users = User.query.count()
    total_admins = User.query.filter_by(role='admin').count()
    total_cashiers = User.query.filter_by(role='staff').count()
    
    return render_template("admin_dashboard.html", 
                         user=current_user,
                         total_users=total_users,
                         total_admins=total_admins,
                         total_cashiers=total_cashiers)

@bp.route('/sales_reports')
@login_required
def sales_reports():
    """Sales Reports page for admins"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get filter parameters
    from datetime import date, timedelta
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    cashier_id = request.args.get('cashier_id', type=int)
    category = request.args.get('category')
    
    # Parse dates
    start_datetime = datetime.fromisoformat(start_date)
    end_datetime = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59)
    
    # Build query
    query = Transaction.query.filter(
        Transaction.date_created >= start_datetime,
        Transaction.date_created <= end_datetime
    )
    
    if cashier_id:
        query = query.filter(Transaction.cashier_id == cashier_id)
    
    transactions = query.order_by(Transaction.date_created.desc()).all()
    
    # Filter by category if specified
    if category:
        transactions = [t for t in transactions if any(sale.product.category == category for sale in t.sales)]
    
    # Calculate summary stats
    total_revenue = sum(t.grand_total for t in transactions) if transactions else 0.0
    total_vat = sum(t.vat_amount for t in transactions) if transactions else 0.0
    total_items = sum(sum(s.quantity for s in t.sales) for t in transactions) if transactions else 0
    total_transactions = len(transactions)
    
    # Get all cashiers for filter dropdown
    cashiers = User.query.filter_by(role='staff').all()
    
    # Get all categories for filter dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('sales_reports.html',
                         user=current_user,
                         transactions=transactions,
                         total_revenue=total_revenue,
                         total_vat=total_vat,
                         total_items=total_items,
                         total_transactions=total_transactions,
                         cashiers=cashiers,
                         categories=categories,
                         start_date=start_date,
                         end_date=end_date,
                         cashier_id=cashier_id,
                         selected_category=category)

@bp.route('/sales_reports_data')
@login_required
def sales_reports_data():
    """API endpoint for chart data"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    from datetime import date, timedelta
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    cashier_id = request.args.get('cashier_id', type=int)
    category = request.args.get('category')
    chart_type = request.args.get('chart_type', 'daily')
    
    # Parse dates
    start_datetime = datetime.fromisoformat(start_date)
    end_datetime = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59)
    
    # Build query
    query = Transaction.query.filter(
        Transaction.date_created >= start_datetime,
        Transaction.date_created <= end_datetime
    )
    
    if cashier_id:
        query = query.filter(Transaction.cashier_id == cashier_id)
    
    transactions = query.all()
    
    # Filter by category if specified
    if category:
        transactions = [t for t in transactions if any(sale.product.category == category for sale in t.sales)]
    
    if chart_type == 'daily':
        # Daily sales chart data
        daily_data = {}
        for t in transactions:
            date_key = t.date_created.date().isoformat()
            if date_key not in daily_data:
                daily_data[date_key] = 0.0
            daily_data[date_key] += t.grand_total
        
        sorted_dates = sorted(daily_data.keys())
        labels = sorted_dates
        data = [daily_data[d] for d in sorted_dates]
        
        return jsonify({
            'labels': labels,
            'data': data,
            'title': 'Daily Sales'
        })
    
    elif chart_type == 'category':
        # Category distribution (pie chart)
        category_data = {}
        for t in transactions:
            for sale in t.sales:
                cat = sale.product.category
                if cat not in category_data:
                    category_data[cat] = 0.0
                category_data[cat] += sale.line_total
        
        labels = list(category_data.keys())
        data = list(category_data.values())
        
        return jsonify({
            'labels': labels,
            'data': data,
            'title': 'Sales by Category'
        })
    
    elif chart_type == 'products':
        # Top products (pie chart)
        product_data = {}
        for t in transactions:
            for sale in t.sales:
                prod = sale.product.name
                if prod not in product_data:
                    product_data[prod] = 0
                product_data[prod] += sale.quantity
        
        # Sort and get top 10
        sorted_products = sorted(product_data.items(), key=lambda x: x[1], reverse=True)[:10]
        labels = [p[0] for p in sorted_products]
        data = [p[1] for p in sorted_products]
        
        return jsonify({
            'labels': labels,
            'data': data,
            'title': 'Top 10 Products by Quantity'
        })
    
    return jsonify({'error': 'Invalid chart type'}), 400

@bp.route('/staff_dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        flash('Access denied: Cashier access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get today's transactions for this cashier
    from datetime import date
    today = date.today()
    today_transactions = Transaction.query.filter(
        Transaction.cashier_id == current_user.id,
        Transaction.date_created >= datetime(today.year, today.month, today.day)
    ).all()
    
    # Calculate summary stats
    total_transactions = len(today_transactions)
    total_sales = sum(t.grand_total for t in today_transactions) if today_transactions else 0.0
    total_items = sum(len(t.sales) for t in today_transactions) if today_transactions else 0
    
    return render_template("staff_dashboard.html", 
                         user=current_user,
                         total_transactions=total_transactions,
                         total_sales=total_sales,
                         total_items=total_items)

# ===== USER MANAGEMENT ROUTES =====

@bp.route('/manage_users')
@login_required
def manage_users():
    """View all users"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    
    return render_template('manage_users.html', 
                         users=users,
                         user=current_user)

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    """Add a new user"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password,
            role=form.role.data
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'User "{form.name.data}" has been added successfully!', 'success')
        return redirect(url_for('main.manage_users'))
    
    return render_template('add_user.html', form=form, user=current_user)

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit a user"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    user_to_edit = User.query.get_or_404(user_id)
    form = EditUserForm()
    form.user_id = user_id
    
    if form.validate_on_submit():
        user_to_edit.name = form.name.data
        user_to_edit.email = form.email.data
        user_to_edit.role = form.role.data
        
        # Only update password if a new one was provided
        if form.password.data:
            user_to_edit.password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        db.session.commit()
        flash(f'User "{user_to_edit.name}" has been updated successfully!', 'success')
        return redirect(url_for('main.manage_users'))
    
    elif request.method == 'GET':
        form.name.data = user_to_edit.name
        form.email.data = user_to_edit.email
        form.role.data = user_to_edit.role
    
    return render_template('edit_user.html', form=form, user=current_user, user_to_edit=user_to_edit)

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    user_to_delete = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user_to_delete.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('main.manage_users'))
    
    user_name = user_to_delete.name
    db.session.delete(user_to_delete)
    db.session.commit()
    
    flash(f'User "{user_name}" has been deleted successfully!', 'success')
    return redirect(url_for('main.manage_users'))

@bp.route('/user_stats')
@login_required
def user_stats():
    """Get user statistics as JSON"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_users = User.query.count()
    total_admins = User.query.filter_by(role='admin').count()
    total_cashiers = User.query.filter_by(role='staff').count()
    
    return jsonify({
        'total_users': total_users,
        'total_admins': total_admins,
        'total_cashiers': total_cashiers
    })


# ===== PRODUCT MANAGEMENT ROUTES =====

@bp.route('/manage_products')
@login_required
def manage_products():
    """View all products"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10)
    
    # Count low stock products
    low_stock_count = Product.query.filter(Product.stock_quantity < 10).count()
    
    return render_template('manage_products.html', 
                         products=products,
                         user=current_user,
                         low_stock_count=low_stock_count)

@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add a new product"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Product(
            product_code=form.product_code.data,
            name=form.name.data,
            category=form.category.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash(f'Product "{form.name.data}" has been added successfully!', 'success')
        return redirect(url_for('main.manage_products'))
    
    return render_template('add_product.html', form=form, user=current_user)

@bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edit a product"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    product_to_edit = Product.query.get_or_404(product_id)
    form = EditProductForm()
    form.product_id = product_id
    
    if form.validate_on_submit():
        product_to_edit.product_code = form.product_code.data
        product_to_edit.name = form.name.data
        product_to_edit.category = form.category.data
        product_to_edit.price = form.price.data
        product_to_edit.stock_quantity = form.stock_quantity.data
        
        db.session.commit()
        flash(f'Product "{product_to_edit.name}" has been updated successfully!', 'success')
        return redirect(url_for('main.manage_products'))
    
    elif request.method == 'GET':
        form.product_code.data = product_to_edit.product_code
        form.name.data = product_to_edit.name
        form.category.data = product_to_edit.category
        form.price.data = product_to_edit.price
        form.stock_quantity.data = product_to_edit.stock_quantity
    
    return render_template('edit_product.html', form=form, user=current_user, product_to_edit=product_to_edit)

@bp.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a product"""
    if current_user.role != 'admin':
        flash('Access denied: Administrator access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    product_to_delete = Product.query.get_or_404(product_id)
    product_name = product_to_delete.name
    
    db.session.delete(product_to_delete)
    db.session.commit()
    
    flash(f'Product "{product_name}" has been deleted successfully!', 'success')
    return redirect(url_for('main.manage_products'))

@bp.route('/restock_product/<int:product_id>', methods=['POST'])
@login_required
def restock_product(product_id):
    """Add stock to a product"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', type=int)
    
    if not quantity or quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    try:
        product.stock_quantity += quantity
        db.session.commit()
        
        flash(f'Added {quantity} units to "{product.name}". New stock: {product.stock_quantity}', 'success')
        return redirect(url_for('main.manage_products'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error restocking product: {str(e)}', 'danger')
        return redirect(url_for('main.manage_products'))

@bp.route('/product_stats')
@login_required
def product_stats():
    """Get product statistics as JSON"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_products = Product.query.count()
    low_stock_products = Product.query.filter(Product.stock_quantity < 10).count()
    total_stock_value = db.session.query(db.func.sum(Product.price * Product.stock_quantity)).scalar() or 0
    
    return jsonify({
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_stock_value': round(float(total_stock_value), 2)
    })


# ===== SALES & BILLING ROUTES =====

@bp.route('/pos')
@login_required
def pos():
    """Point of Sale interface for cashiers"""
    if current_user.role != 'staff':
        flash('Access denied: Cashier access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = []
    
    form = SearchProductForm()
    search_results = []
    
    # Search for products
    if form.validate_on_submit() and form.search_query.data:
        search_query = form.search_query.data.lower()
        search_results = Product.query.filter(
            (Product.name.ilike(f'%{search_query}%')) |
            (Product.product_code.ilike(f'%{search_query}%'))
        ).all()
    else:
        # Show all products if no search
        search_results = Product.query.all()
    
    # Calculate cart totals
    subtotal = sum(item['unit_price'] * item['quantity'] for item in session.get('cart', []))
    vat = subtotal * 0.15  # 15% VAT
    grand_total = subtotal + vat
    
    return render_template('pos.html', 
                         products=search_results,
                         form=form,
                         cart=session.get('cart', []),
                         subtotal=subtotal,
                         vat=vat,
                         grand_total=grand_total,
                         user=current_user)

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add item to shopping cart"""
    if current_user.role != 'staff':
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)
    
    # Validate quantity
    if quantity < 1:
        return jsonify({'error': 'Quantity must be at least 1'}), 400
    
    if quantity > product.stock_quantity:
        return jsonify({'error': f'Insufficient stock. Available: {product.stock_quantity}'}), 400
    
    # Initialize cart if needed
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if product already in cart
    cart_item = None
    for item in session['cart']:
        if item['product_id'] == product_id:
            cart_item = item
            break
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item['quantity'] + quantity
        if new_quantity > product.stock_quantity:
            return jsonify({'error': f'Insufficient stock. Available: {product.stock_quantity}'}), 400
        cart_item['quantity'] = new_quantity
    else:
        # Add new item to cart
        session['cart'].append({
            'product_id': product_id,
            'product_code': product.product_code,
            'product_name': product.name,
            'unit_price': product.price,
            'quantity': quantity,
            'is_low_stock': product.is_low_stock()
        })
    
    session.modified = True
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('main.pos'))

@bp.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    """Update cart item quantity"""
    if current_user.role != 'staff':
        return jsonify({'error': 'Unauthorized'}), 403
    
    quantity = request.form.get('quantity', 1, type=int)
    product = Product.query.get_or_404(product_id)
    
    if quantity < 1:
        return jsonify({'error': 'Quantity must be at least 1'}), 400
    
    if quantity > product.stock_quantity:
        flash(f'Insufficient stock. Available: {product.stock_quantity}', 'danger')
        return redirect(url_for('main.pos'))
    
    for item in session.get('cart', []):
        if item['product_id'] == product_id:
            item['quantity'] = quantity
            break
    
    session.modified = True
    flash(f'{product.name} quantity updated!', 'success')
    return redirect(url_for('main.pos'))

@bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    """Remove item from cart"""
    if current_user.role != 'staff':
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(product_id)
    session['cart'] = [item for item in session.get('cart', []) if item['product_id'] != product_id]
    session.modified = True
    
    flash(f'{product.name} removed from cart!', 'success')
    return redirect(url_for('main.pos'))

@bp.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    """Clear entire cart"""
    if current_user.role != 'staff':
        return jsonify({'error': 'Unauthorized'}), 403
    
    session['cart'] = []
    session.modified = True
    
    flash('Cart cleared!', 'info')
    return redirect(url_for('main.pos'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Complete the sale and generate receipt"""
    if current_user.role != 'staff':
        flash('Access denied: Cashier access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    cart = session.get('cart', [])
    
    if not cart:
        flash('Cart is empty. Add items before checkout.', 'danger')
        return redirect(url_for('main.pos'))
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        try:
            # Calculate totals
            subtotal = sum(item['unit_price'] * item['quantity'] for item in cart)
            vat = subtotal * 0.15  # 15% VAT
            grand_total = subtotal + vat
            
            # Create transaction
            transaction = Transaction(
                cashier_id=current_user.id,
                subtotal=subtotal,
                vat_amount=vat,
                grand_total=grand_total,
                payment_method=form.payment_method.data,
                status='completed'
            )
            
            db.session.add(transaction)
            db.session.flush()  # Get transaction ID
            
            # Create sales and update stock
            for item in cart:
                product = Product.query.get(item['product_id'])
                
                # Create sale record
                sale = Sale(
                    transaction_id=transaction.id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    line_total=item['unit_price'] * item['quantity']
                )
                
                # Update product stock
                product.stock_quantity -= item['quantity']
                
                db.session.add(sale)
            
            # Commit all changes
            db.session.commit()
            
            # Clear cart
            session['cart'] = []
            session.modified = True
            
            flash('Sale completed successfully!', 'success')
            return redirect(url_for('main.receipt', transaction_id=transaction.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing sale: {str(e)}', 'danger')
            return redirect(url_for('main.pos'))
    
    # Calculate totals for display
    subtotal = sum(item['unit_price'] * item['quantity'] for item in cart)
    vat = subtotal * 0.15
    grand_total = subtotal + vat
    
    return render_template('checkout.html',
                         form=form,
                         cart=cart,
                         subtotal=subtotal,
                         vat=vat,
                         grand_total=grand_total,
                         user=current_user)

@bp.route('/receipt/<int:transaction_id>')
@login_required
def receipt(transaction_id):
    """Display receipt for completed transaction"""
    if current_user.role != 'staff':
        flash('Access denied: Cashier access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Verify cashier owns this transaction
    if transaction.cashier_id != current_user.id:
        flash('You can only view your own receipts.', 'danger')
        return redirect(url_for('main.pos'))
    
    sales = Sale.query.filter_by(transaction_id=transaction_id).all()
    
    return render_template('receipt.html',
                         transaction=transaction,
                         sales=sales,
                         user=current_user)

@bp.route('/sales_history')
@login_required
def sales_history():
    """View transaction history"""
    if current_user.role != 'staff':
        flash('Access denied: Cashier access required.', 'danger')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.filter(
        Transaction.cashier_id == current_user.id
    ).order_by(
        Transaction.date_created.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('sales_history.html',
                         transactions=transactions,
                         user=current_user)






