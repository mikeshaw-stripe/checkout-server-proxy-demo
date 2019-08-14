from flask import Flask
from flask import render_template
from dotenv import load_dotenv
import os
import stripe

load_dotenv()

app = Flask(__name__)

stripe.api_key = os.getenv('STRIPE_SKEY')

@app.route('/')
def index():
  # Creates a new Stripe Checkout Session
  print('Creating a Checkout Session')
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'name': 'T-shirt',
      'description': 'Comfortable cotton t-shirt',
      'images': ['https://example.com/t-shirt.png'],
      'amount': 500,
      'currency': 'eur',
      'quantity': 1,
    }],
    success_url='{}/success'.format(os.getenv('DOMAIN')),
    cancel_url='{}/cancel'.format(os.getenv('DOMAIN')),
  )

  return render_template('index.html', DOMAIN=os.getenv('DOMAIN'), CHECKOUT_SESSION_ID=session.id)

@app.route('/success')
def success():
  return 'Payment Succeeded'

@app.route('/cancel')
def cancle():
  return 'Payment Cancelled'

@app.route('/pay/<session>')
def pay(session):
  return render_template('pay.html', CHECKOUT_SESSION_ID=session, STRIPE_PKEY=os.getenv('STRIPE_PKEY'))