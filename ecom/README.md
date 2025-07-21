# 🛒 Django eCommerce Platform

A full-featured Django-based eCommerce web application with product variations, coupon support, cart & checkout flow, and order management with **Cash on Delivery (COD)** as the default payment method. Includes a secure admin panel for complete control.

---

## 📁 Project Structure

```
/django-ecommerce
│
├── ecom/                  → Django project settings and URLs
├── base/                  → Main app: models, views, URLs, templates
├── public/                → Static files: CSS, JS, fonts, etc.
├── Home/                  → Homepage modals, views, templates
├── accounts/               → Account modals, views, templates
├── product/               → Product modals, views, templates
├── templates/             → Base and app-specific templates
├── manage.py              → Django management script
└── README.md              → This file
```

---

## 🧩 Key Features

- 🔐 Secure user authentication and profile management
- 🛍️ Product variations (color, size) with dynamic pricing
- 🛒 Cart and checkout functionality with coupon support
- 📦 Order management with statuses (Pending, Shipped, Delivered)
- 💵 Cash on Delivery (COD) payment method
- 📜 Admin panel for managing products, orders, coupons, etc.

---

## ⚙️ Technologies Used

| Tech                | Version  | Description             |
| ------------------- | -------- | ----------------------- |
| Python              | 3.10+    | Programming language    |
| Django              | 4.2+     | Main web framework      |
| SQLite / PostgreSQL | any      | Database backend        |
| Bootstrap           | 5        | Frontend styling        |
| Pillow              | latest   | Image processing        |
| Django Crispy Forms | optional | Enhanced form rendering |

---

## 🛠 Installation & Setup

### 🔹 Prerequisites

- Python 3.10 or newer
- pip
- Git

### 🔹 Clone the Repository

```bash
git clone https://github.com/yourusername/django-ecommerce.git
cd django-ecommerce
```

### 🔹 Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate        # Linux/Mac
env\Scripts\activate           # Windows
```

### 🔹 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 🔹 Create Superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 🔹 Run the Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`  
Admin: `http://127.0.0.1:8000/admin/`

---

## 🧪 Sample Admin Panel Features

- Add/Edit/Delete Products
- Manage Variations (Color, Size)
- Manage Coupons
- View & update Order Status
- Manage Users

---

## 💳 Payment

- 💵 **Cash on Delivery (COD)** is implemented as the default method.
- Placeholder for future integration of Stripe, PayPal, or other gateways.

---

## 📤 Deployment Suggestions

- Use **Gunicorn** and **Nginx** for production
- Use **PostgreSQL** in production
- Set `DEBUG=False` and configure `ALLOWED_HOSTS`
- Configure static/media file handling
- Use **env vars** to manage secret keys and database credentials

---

## 🧱 Database Models Summary

- **User** → Profile (1:1)
- **User** → Cart / Order (1:N)
- **Product** → Category / Size / Color / Images
- **Cart** → Items / Coupon (1:N)
- **Order** → Cart (1:1)

Detailed schema is based on the design document.

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.

---

## 🙋‍♂️ Author

**Muhammad Zayem**  
[GitHub](https://github.com/mzayem)
