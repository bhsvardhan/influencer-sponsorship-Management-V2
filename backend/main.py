import sqlite3,os,re
from flask import Flask, render_template, request, jsonify, redirect, session
from flask import *
from datetime import datetime
from flask_cors import CORS
from flask_caching import Cache
app = Flask(__name__)
CORS(app)
app.secret_key = "asdlkjqwepoirtyiuyzxc,mncvbnbv0912398735=-0`12"
abs = os.path.abspath(__file__)
uploadPath = abs[0:-9]+"uploads"
app.config['UPLOAD_FOLDER'] = uploadPath
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@cache.cached(timeout=10000)
@app.route('/logOut',methods=['GET'])
def logOut():
  session['user']=None
  session['role']=None
  return jsonify({"SUCCESS":"Logout successful!"}), 200

@cache.cached(timeout=10000)
@app.route('/sponsor_register', methods=['POST'])
def sponsor_register():
    data = request.json  # Handle JSON data from frontend
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    industry = data.get('industry')
    budget = data.get('budget')

    # Ensure that all required fields are provided
    if not all([username, password, name, industry, budget]):
        return jsonify({"BAD_REQUEST": "Missing required fields"}), 400

    regex = r"^[a-zA-Z0-9]{8,}$"  # Regex for password (at least 8 alphanumeric characters)

    # Validate the password format
    if not re.match(regex, password):
        return jsonify({"BAD_REQUEST": "Password must be at least 8 characters long and contain only alphanumeric characters!"}), 400

    # Connect to the database
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        # Insert into sponsor_users table
        cur.execute('''
            INSERT INTO sponsor_users (username, password, name, industry, budget)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, name, industry, budget))
        
        # Insert into users table with a role of 2 for sponsor
        cur.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', (username, password, 2))
        
        # Commit the transaction
        conn.commit()
        print("Sponsor user added successfully!")

        return jsonify({"SUCCESS": "User created successfully!"}), 200

    except sqlite3.IntegrityError:
        # This error is raised when trying to insert a duplicate username
        return jsonify({"ERROR": "User Already Exists"}), 400
    except Exception as e:
        # Handle any other exceptions
        print(f"Error while adding data to the database: {e}")
        return jsonify({"ERROR": "An error occurred while processing your request."}), 500
    finally:
        # Ensure the cursor and connection are closed properly
        cur.close()
        conn.close()

@cache.cached(timeout=10000)
@app.route('/influencer_register', methods=['POST'])
def influencer_register():
    data = request.json  # Handle JSON data from frontend
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    niche = data.get('niche')
    category = data.get('category')
    reach = data.get('reach')
    phonenumber = data.get('phoneNumber')
    platform_presence = data.get('platform_presence')

    # Ensure that all required fields are provided
    if not all([username, password, name, niche, category, reach, phonenumber, platform_presence]):
        return jsonify({"BAD_REQUEST": "Missing required fields"}), 400

    regex = r"^[a-zA-Z0-9]{8,}$"  # Regex for password (at least 8 alphanumeric characters)

    # Validate the password format
    if not re.match(regex, password):
        return jsonify({"BAD_REQUEST": "Password must be at least 8 characters long and contain only alphanumeric characters!"}), 400

    # Connect to the database
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        # Insert into influencer_users table
        cur.execute('''
            INSERT INTO influencer_users1 (username, password, name, niche, category, reach, platform_presence, phonenumber)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, name, niche, category, reach, platform_presence, phonenumber))
        
        # Insert into users table with a role of 3 for influencer
        cur.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', (username, password, 3))
        
        # Commit the transaction
        conn.commit()
        print("Influencer user added successfully!")

        return jsonify({"SUCCESS": "User created successfully!"}), 200

    except sqlite3.IntegrityError:
        # This error is raised when trying to insert a duplicate username
        return jsonify({"ERROR": "User Already Exists"}), 400
    except Exception as e:
        # Handle any other exceptions
        print(f"Error while adding data to the database: {e}")
        return jsonify({"ERROR": "An error occurred while processing your request."}), 500
    finally:
        # Ensure the cursor and connection are closed properly
        cur.close()
        conn.close()


@cache.cached(timeout=10000)
@app.route("/loginUser", methods=["POST"])
def loginUser():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if(username=="" or password==""):
        return jsonify({"BAD_REQUEST":"Invalid credentials!"}), 400
    print(username,password)
    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password))
            data = cur.fetchall()
            print(data)
            role = data[0][-1]
            session["user"] = username
            session["role"] = role
            cache.clear()
            print("User found successfully!")
            if role == 1:
                return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
            elif role == 2:
                return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
            elif role == 3:
                return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
    except Exception as e:
        print("User data not found in database",str(e))
        return jsonify({"ERROR":"User data not found in database"}), 400
  

@cache.cached(timeout=10000)
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT name, 'campaign' AS type, start_date, end_date FROM campaigns WHERE end_date >= date('now')")
        campaigns = cur.fetchall()

        cur.execute("SELECT name, type FROM flagged_users_campaigns")
        flagged_items = cur.fetchall()

        campaign_list = [
            {"name": campaign[0], "type": campaign[1], "start_date": campaign[2], "end_date": campaign[3]}
            for campaign in campaigns
        ]

        flagged_items_list = [
            {"name": item[0], "type": item[1]}
            for item in flagged_items
        ]

        return jsonify({
            "user": session.get('user'),
            "campaigns": campaign_list,
            "flagged_items": flagged_items_list
        }), 200
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
    finally:
        conn.close()
    

@cache.cached(timeout=10000)  
@app.route('/admin_dashboard1', methods=['GET'])
def admin_dashboard1():

    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        search_query = request.args.get('search_query', '')  # Use `args` for GET requests
        results = []

        if search_query:
            # Search in campaigns
            cur.execute(
                "SELECT name, 'campaign' AS type, name AS id FROM campaigns WHERE name LIKE ?",
                ('%' + search_query + '%',),
            )
            results.extend(cur.fetchall())

            # Search in influencer_users
            cur.execute(
                "SELECT name, 'influencer' AS type, username AS id FROM influencer_users WHERE name LIKE ?",
                ('%' + search_query + '%',),
            )
            results.extend(cur.fetchall())

            # Search in sponsor_users
            cur.execute(
                "SELECT name, 'sponsor' AS type, username AS id FROM sponsor_users WHERE name LIKE ?",
                ('%' + search_query + '%',),
            )
            results.extend(cur.fetchall())
        else:
            # No search query, just show all
            cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns")
            results.extend(cur.fetchall())

            cur.execute("SELECT name, 'influencer' AS type, username AS id FROM influencer_users")
            results.extend(cur.fetchall())

            cur.execute("SELECT name, 'sponsor' AS type, username AS id FROM sponsor_users")
            results.extend(cur.fetchall())

        # Convert results into a JSON-serializable format
        results_json = [{"name": row[0], "type": row[1], "id": row[2]} for row in results]

        return jsonify({"user": session.get('user'), "results": results_json}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    finally:
        conn.close()

@cache.cached(timeout=10000)
@app.route('/api/stats', methods=['GET'])
def api_stats():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Example statistics queries
    cur.execute("SELECT COUNT(*) AS total_campaigns FROM campaigns")
    total_campaigns = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) AS total_influencers FROM influencer_users1")
    total_influencers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) AS total_sponsors FROM sponsor_users")
    total_sponsors = cur.fetchone()[0]

    cur.execute("SELECT SUM(budget) AS total_budget FROM campaigns")
    total_budget = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) AS total_requests FROM ad_requests1")
    total_requests = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) AS total_accepted_requests FROM ad_requests1 WHERE status='accepted'")
    total_accepted_requests = cur.fetchone()[0]

    stats = {
        'total_campaigns': total_campaigns,
        'total_influencers': total_influencers,
        'total_sponsors': total_sponsors,
        'total_budget': total_budget,
        'total_requests': total_requests,
        'total_accepted_requests': total_accepted_requests,
    }

    conn.close()
    return jsonify(stats)

@cache.cached(timeout=10000)
@app.route('/remove_flagged/<name>', methods=['DELETE'])
def remove_flagged(name):
    

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM flagged_users_campaigns WHERE name = ?", (name,))
        conn.commit()

        if cur.rowcount > 0:
            return jsonify({"message": f"{name} has been successfully removed."}), 200
        else:
            return jsonify({"error": "Item not found or already removed."}), 404
    except Exception as e:
        return jsonify({"error": "Failed to remove flagged item", "details": str(e)}), 500
    finally:
        conn.close()

@cache.cached(timeout=10000)
@app.route('/flag/<item_id>', methods=['GET','POST'])
def flag_item(item_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Identify the type of item
    cur.execute("SELECT 'campaign' AS type FROM campaigns WHERE name = ?", (item_id,))
    item = cur.fetchone()
    if not item:
        cur.execute("SELECT 'influencer' AS type FROM influencer_users WHERE username = ?", (item_id,))
        item = cur.fetchone()
    if not item:
        cur.execute("SELECT 'sponsor' AS type FROM sponsor_users WHERE username = ?", (item_id,))
        item = cur.fetchone()

    if item:
        type_ = item[0]

        # Add to flagged table
        cur.execute("INSERT INTO flagged_users_campaigns (name, type) VALUES (?, ?)", (item_id, type_))

        # Remove from original table
        if type_ == 'campaign':
            cur.execute("DELETE FROM campaigns WHERE name = ?", (item_id,))
        elif type_ == 'influencer':
            cur.execute("DELETE FROM influencer_users WHERE username = ?", (item_id,))
        elif type_ == 'sponsor':
            cur.execute("DELETE FROM sponsor_users WHERE username = ?", (item_id,))
        
        # Remove from users table
        cur.execute("DELETE FROM users WHERE username = ?", (item_id,))
        
        conn.commit()
        conn.close()

        # Return JSON response
        return jsonify({
            "status": "success",
            "message": f"{type_.capitalize()} '{item_id}' has been flagged and removed.",
            "type": type_,
            "item_id": item_id
        }), 200
    else:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Item not found.",
            "item_id": item_id
        }), 404

@cache.cached(timeout=10000)
@app.route('/current_campaigns', methods=['GET','POST'])
def get_current_campaigns():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    cur = conn.cursor()

    try:
        # Query to fetch campaigns
        cur.execute("""
            SELECT *
            FROM campaigns 
            WHERE end_date >= date('now')
            ORDER BY start_date DESC
        """)

        rows = cur.fetchall()
        print("Debug - Raw campaigns data:", [dict(row) for row in rows])  # Debug print

        # Convert rows to a list of dictionaries
        campaigns = [
            {
                "name": row['name'],
                "description": row['description'],
                "start_date": row['start_date'],
                "end_date": row['end_date'],
                "budget": row['budget'],
                "visibility": row['visibility'],
                "goals": row['goals']
            }
            for row in rows
        ]
        
        print("Debug - Processed campaigns:", campaigns)  # Debug print
        return campaigns  # Return the data, not a Response object
    except Exception as e:
        print("Debug - Error in current_campaigns:", str(e))  # Debug print
        raise e  # Let the caller handle exceptions
    finally:
        conn.close()

@cache.cached(timeout=10000)
@app.route('/flagged_users_campaigns', methods=['GET'])
def get_flagged_users_campaigns():

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # Simple select all query
        cur.execute("""
            SELECT * 
            FROM flagged_users_campaigns 
            ORDER BY flag_date DESC
        """)
        
        rows = cur.fetchall()
        print("Debug - Raw flagged data:", [dict(row) for row in rows])  # Debug print
        
        flagged = []
        for row in rows:
            flagged.append({
                "name": row['name'],
                "type": row['type'],
                "flag_date": row['flag_date']
            })
            
        print("Debug - Processed flagged items:", flagged)  # Debug print
        return jsonify(flagged), 200
    except Exception as e:
        print("Debug - Error in flagged_users_campaigns:", str(e))  # Debug print
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# Function to get current campaigns
@cache.cached(timeout=10000)
@app.route('/influencer_dashboard', methods=['GET','POST'])
def influencer_dashboard():
    try:
        campaigns = get_current_campaigns()  # Replace with your actual logic for campaigns
        user_name = session.get('user')
        return jsonify({"campaigns": campaigns, "name": user_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# View requests for the influencer
@cache.cached(timeout=10000)
@app.route('/view_requests_influencer', methods=['GET'])
def view_requests_influencer():
    # Get the influencer_username from query parameters
    influencer_username = request.args.get('influencer_username')

    if not influencer_username:
        return jsonify({"error": "Influencer username is required"}), 400

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Fetch pending ad requests specific to the influencer
    cur.execute("""
        SELECT 
            campaign_name, 
            influencer_username, 
            sponsor_username, 
            messages, 
            requirements, 
            payment_amount, 
            status 
        FROM ad_requests1 
        WHERE status='pending' AND influencer_username=?
    """, (influencer_username,))
    
    requests = cur.fetchall()
    conn.close()

    # Format the requests into a list of dictionaries
    formatted_requests = [
        {
            "campaign_name": row[0],
            "influencer_username": row[1],
            "sponsor_username": row[2],
            "messages": row[3],
            "requirements": row[4],
            "payment_amount": row[5],
            "status": row[6],
        }
        for row in requests
    ]

    return jsonify({"requests": formatted_requests})



# Find a campaign by name
@cache.cached(timeout=10000)
@app.route('/find_campaign', methods=['POST'])
def find_campaign():
    data = request.json
    campaign_name = data.get('campaign_name')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM campaigns WHERE name = ?', (campaign_name,))
        campaign = cur.fetchone()
        conn.close()

        if campaign:
            # Convert campaign data to a JSON-compatible structure
            campaign_info = {
                "id": campaign[0],
                "name": campaign[1],
                "details": campaign[2],
                # Add other fields as necessary
            }
            return jsonify({"campaign_info": campaign_info})
        else:
            return jsonify({"error": "Campaign not found"}), 404
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500


# Accept a request as an influencer
@cache.cached(timeout=10000)
@app.route('/accept_request_influencer', methods=['POST'])
def accept_request_influencer():


    data = request.json
    campaign_name = data.get('campaign_name')
    influencer_username = data.get('influencer_username')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        # Retrieve the sponsor_username based on campaign_name and influencer_username
        cur.execute("""
            SELECT sponsor_username
            FROM ad_requests1
            WHERE campaign_name = ? AND influencer_username = ?
        """, (campaign_name, influencer_username))
        
        sponsor_username = cur.fetchone()

        if sponsor_username:
            sponsor_username = sponsor_username[0]

            # Update the status to 'accepted'
            cur.execute("""
                UPDATE ad_requests1
                SET status = 'accepted'
                WHERE campaign_name = ? AND influencer_username = ?
            """, (campaign_name, influencer_username))

            # Insert into the events table
            cur.execute("""
                INSERT INTO events(campaign_name, influencer_username, sponsor_username)
                VALUES (?, ?, ?)
            """, (campaign_name, influencer_username, sponsor_username))

            conn.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Request not found"}), 404
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Reject a request as an influencer
@cache.cached(timeout=10000)
@app.route('/reject_request_influencer', methods=['POST'])
def reject_request_influencer():
    if session.get('role') is None:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.json
    campaign_name = data.get('campaign_name')
    influencer_username = data.get('influencer_username')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE ad_requests1
            SET status = 'rejected'
            WHERE campaign_name = ? AND influencer_username = ?
        """, (campaign_name, influencer_username))
        
        conn.commit()
        return jsonify({"success": True})
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@cache.cached(timeout=10000)
@app.route('/create_adrequest', methods=['GET', 'POST'])
def create_adrequest():
    if(session.get('role') !=3):
        return render_template("unAuth.html")
    if request.method == 'POST':
        campaign_name = request.form['campaign_name']
        influencer_username = request.form['influencer_username']
        message = request.form['message']
        requirements = request.form['requirements']
        payment_amount = request.form['payment_amount']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ad_requests1 (campaign_name, influencer_username, messages, requirements, payment_amount, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (campaign_name, influencer_username, message, requirements, payment_amount))
        conn.commit()
        conn.close()

        return redirect(url_for('create_adrequest'))  # Redirect to the same form or another page after submission

    return render_template('create_adrequest.html')

@cache.cached(timeout=10000)
@app.route('/all_data1', methods=['GET'])
def all_data1():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    results = []

    # Fetch all data from campaigns
    cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns")
    results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

    # Fetch all data from influencer_users
    cur.execute("SELECT username AS name, 'influencer' AS type, username AS id FROM influencer_users1")
    results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

    conn.close()
    return jsonify(results)

@cache.cached(timeout=10000)
@app.route('/all_data2', methods=['GET'])
def all_data2():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    results = []

    # Fetch all data from campaigns
    cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns")
    results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

    # Fetch all data from influencer_users
    cur.execute("SELECT username AS name, 'sponsor' AS type, username AS id FROM sponsor_users")
    results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

    conn.close()
    return jsonify(results)

@app.route('/search2', methods=['GET'])
def search2():
    query = request.args.get('query', '')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    results = []

    if query:
        # Search in campaigns
        cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns WHERE name LIKE ?", ('%' + query + '%',))
        results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

        # Search in influencer_users
        cur.execute("SELECT username AS name, 'sponsor' AS type, username AS id FROM sponsor_users WHERE username LIKE ?", ('%' + query + '%',))
        results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

    conn.close()
    return jsonify(results)

@app.route('/search1', methods=['GET'])
def search1():
    query = request.args.get('query', '')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    results = []

    if query:
        # Search in campaigns
        cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns WHERE name LIKE ?", ('%' + query + '%',))
        results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

        # Search in influencer_users
        cur.execute("SELECT username AS name, 'influencer' AS type, username AS id FROM influencer_users1 WHERE username LIKE ?", ('%' + query + '%',))
        results.extend([{'name': row[0], 'type': row[1], 'id': row[2]} for row in cur.fetchall()])

    conn.close()
    return jsonify(results)

@app.route('/view_campaign1/<campaign_id>', methods=['GET'])
def view_campaign1(campaign_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM campaigns WHERE name = ?", (campaign_id,))
    campaign = cur.fetchone()
    conn.close()
    
    if campaign:
        keys = [description[0] for description in cur.description]
        campaign_data = dict(zip(keys, campaign))
        return jsonify(campaign_data)
    else:
        return jsonify({"error": "Campaign not found"}), 404

@app.route('/view_influencer1/<influencer_id>', methods=['GET'])
def view_influencer1(influencer_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM influencer_users1 WHERE username = ?", (influencer_id,))
    influencer = cur.fetchone()
    conn.close()
    
    if influencer:
        keys = [description[0] for description in cur.description]
        influencer_data = dict(zip(keys, influencer))
        return jsonify(influencer_data)
    else:
        return jsonify({"error": "Influencer not found"}), 404
    
@app.route('/view_sponsor1/<sponsor_id>', methods=['GET'])
def view_sponsor1(sponsor_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sponsor_users WHERE username = ?", (sponsor_id,))
    sponsor = cur.fetchone()
    conn.close()
    
    if sponsor:
        keys = [description[0] for description in cur.description]
        sponsor_data = dict(zip(keys, sponsor))
        return jsonify(sponsor_data)
    else:
        return jsonify({"error": "Sponsor not found"}), 404

@app.route('/send_request1/<influencer_id>', methods=['POST'])
def send_request1(influencer_id):
    data = request.get_json()
    campaign_name = data['campaign_name']
    sponsor_name = data.get('sponsorUsername')
    message = data['message']
    requirements = data['requirements']
    payment_amount = data['payment_amount']
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ad_requests1 (campaign_name,sponsor_username, influencer_username, messages, requirements, payment_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
    """, (campaign_name,sponsor_name, influencer_id, message, requirements, payment_amount))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@app.route('/send_request2/<sponsor_id>', methods=['POST'])
def send_request2(sponsor_id):
    data = request.get_json()
    campaign_name = data['campaign_name']
    influencer_name=data.get('influencerUsername')
    message = data['message']
    requirements = data['requirements']
    payment_amount = data['payment_amount']
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ad_requests (campaign_name,influencer_username, sponsor_username, messages, requirements, payment_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
    """, (campaign_name,influencer_name, sponsor_id, message, requirements, payment_amount))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@app.route('/all_data', methods=['GET'])
def all_data():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    results = []

    # Fetch all data from campaigns
    cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns")
    results.extend(cur.fetchall())

    # Fetch all data from influencer_users
    cur.execute("SELECT name, 'influencer' AS type, username AS id FROM influencer_users1")
    results.extend(cur.fetchall())

    # Fetch all data from sponsor_users
    cur.execute("SELECT name, 'sponsor' AS type, username AS id FROM sponsor_users")
    results.extend(cur.fetchall())

    conn.close()
    return jsonify(results)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    results = []

    if query:
        # Search in campaigns
        cur.execute("SELECT name, 'campaign' AS type, name AS id FROM campaigns WHERE name LIKE ?", ('%' + query + '%',))
        results.extend(cur.fetchall())

        # Search in influencer_users
        cur.execute("SELECT name, 'influencer' AS type, username AS id FROM influencer_users1 WHERE name LIKE ?", ('%' + query + '%',))
        results.extend(cur.fetchall())

        # Search in sponsor_users
        cur.execute("SELECT name, 'sponsor' AS type, username AS id FROM sponsor_users WHERE name LIKE ?", ('%' + query + '%',))
        results.extend(cur.fetchall())

    conn.close()
    return jsonify(results)

@app.route('/view/<item_id>', methods=['GET','POST'])
def view_item(item_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Determine the type of the item
    cur.execute("SELECT 'campaign' AS type FROM campaigns WHERE name = ?", (item_id,))
    item = cur.fetchone()
    if not item:
        cur.execute("SELECT 'influencer' AS type FROM influencer_users1 WHERE username = ?", (item_id,))
        item = cur.fetchone()
    if not item:
        cur.execute("SELECT 'sponsor' AS type FROM sponsor_users WHERE username = ?", (item_id,))
        item = cur.fetchone()

    if item:
        type_ = item[0]

        # Fetch details based on type
        if type_ == 'campaign':
            cur.execute("SELECT * FROM campaigns WHERE name = ?", (item_id,))
        elif type_ == 'influencer':
            cur.execute("SELECT * FROM influencer_users1 WHERE username = ?", (item_id,))
        elif type_ == 'sponsor':
            cur.execute("SELECT * FROM sponsor_users WHERE username = ?", (item_id,))

        item_data = cur.fetchone()
        conn.close()

        if item_data:
            return jsonify({
                "status": "success",
                "type": type_,
                "item_data": item_data
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Item details not found."
            }), 404
    else:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Item not found."
        }), 404



@app.route('/search_campaigns', methods=['GET'])
def search_campaigns():
    search_query = request.args.get('search', '').lower()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM campaigns WHERE LOWER(name) LIKE ?", (search_query + '%',))
    campaigns = cur.fetchall()
    conn.close()
    return jsonify(campaigns)

@app.route('/api/add_campaign', methods=['POST'])
def add_campaign():

    data = request.json
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    budget = data.get('budget')
    visibility = data.get('visibility')
    goals = data.get('goals')

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        cur.execute('''
            INSERT INTO campaigns(name, description, start_date, end_date, budget, visibility, goals)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, start_date, end_date, budget, visibility, goals))
        conn.commit()
        return jsonify({"message": "Campaign added successfully"}), 200

    except sqlite3.IntegrityError:
        return jsonify({"error": "Campaign with the same name already exists"}), 409

    finally:
        cur.close()
        conn.close()


@app.route('/send_request', methods=['POST'])
def send_request():
    
    data = request.json
    campaign_name = data['campaign_name']
    influencer_username = session.get('user')  # Get the actual logged-in influencer's username from session
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO ad_requests (campaign_name, influencer_username, status)
            VALUES (?, ?, 'pending')
        ''', (campaign_name, influencer_username))
        conn.commit()
        return jsonify({'message': 'Request sent successfully!'}), 200
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Request already exists'}), 409
    finally:
        cur.close()
        conn.close()


@app.route('/api/view_requests', methods=['GET'])
def view_requests():
    # Fetch campaigns from a hypothetical function
    campaigns = get_current_campaigns()

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Fetch pending ad requests with all details
    cur.execute("""
        SELECT 
            campaign_name, 
            influencer_username, 
            sponsor_username, 
            messages, 
            requirements, 
            payment_amount, 
            status 
        FROM ad_requests 
        WHERE status='pending'
    """)
    requests = cur.fetchall()
    conn.close()

    # Build the JSON response
    response_data = {
        "name": session.get('user'),
        "campaigns": campaigns,
        "requests": [
            {
                "campaign_name": req[0],
                "influencer_username": req[1],
                "sponsor_username": req[2],
                "messages": req[3],
                "requirements": req[4],
                "payment_amount": req[5],
                "status": req[6],
            } 
            for req in requests
        ],
    }

    return jsonify(response_data)


@app.route('/api/accept_request', methods=['POST'])
def accept_request():
    # Parse JSON data from the request
    data = request.get_json()
    if not data or 'campaign_name' not in data or 'influencer_username' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    campaign_name = data['campaign_name']
    influencer_username = data['influencer_username']
    sponsor_username = session.get('user')  # Retrieve the logged-in sponsor

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        # Update the request status to 'accepted'
        cur.execute('''
            UPDATE ad_requests
            SET status = 'accepted'
            WHERE campaign_name = ? AND influencer_username = ? AND status = 'pending'
        ''', (campaign_name, influencer_username))


        # Insert the new event into the `events` table
        cur.execute('''
            INSERT INTO events (campaign_name, influencer_username, sponsor_username)
            VALUES (?, ?, ?)
        ''', (campaign_name, influencer_username, sponsor_username))

        conn.commit()

        return jsonify({"message": "Request accepted successfully!"}), 200

    except sqlite3.IntegrityError as e:
        return jsonify({"error": "Failed to accept request", "details": str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cur.close()
        conn.close()




@app.route('/api/sponsor_dashboard', methods=['GET'])
def sponsor_dashboard():

    # Fetch campaigns from a hypothetical function
    campaigns = get_current_campaigns()
    if campaigns is None:
        campaigns = []

    # Ensure campaigns are JSON-serializable
    if isinstance(campaigns, list):
        campaigns = [{"id": c[0], "name": c[1]} if isinstance(c, tuple) else c for c in campaigns]

    # Connect to the database
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Enable named column access
    cur = conn.cursor()

    try:
        # Fetch pending ad requests
        cur.execute("""
            SELECT campaign_name, influencer_username 
            FROM ad_requests 
            WHERE status='pending'
        """)
        requests = cur.fetchall()

        # Ensure requests are JSON-serializable
        formatted_requests = [
            {"campaign_name": req["campaign_name"], "influencer_username": req["influencer_username"]}
            for req in requests
        ]

        # Build the response data
        response_data = {
            "name": session.get('user'),
            "campaigns": campaigns,
            "requests": formatted_requests,
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

    finally:
        conn.close()


@app.route('/api/reject_request', methods=['POST'])
def reject_request():
    # Parse JSON data from the request
    data = request.get_json()
    if not data or 'campaign_name' not in data or 'influencer_username' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    campaign_name = data['campaign_name']
    influencer_username = data['influencer_username']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        # Update the request status to 'rejected'
        cur.execute('''
            UPDATE ad_requests
            SET status = 'rejected'
            WHERE campaign_name = ? AND influencer_username = ?
        ''', (campaign_name, influencer_username))
        conn.commit()

        return jsonify({"message": "Request rejected successfully!"}), 200

    except sqlite3.Error as e:
        # Return error details if a database error occurs
        return jsonify({"error": "Failed to reject request", "details": str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cur.close()
        conn.close()



@app.route('/campaign/<campaign_name>', methods=['GET'])
def view_campaign(campaign_name):
    if(session.get('role') == None):
        return render_template("unAuth.html")
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM campaigns WHERE name=?", (campaign_name,))
    campaign = cur.fetchone()
    conn.close()
    return render_template('view_campaign.html', campaign=campaign)


@app.route('/api/find_influencer', methods=['POST'])
def find_influencer():
    # Check if the user is authorized
    if session.get('role') is None:
        return jsonify({"error": "Unauthorized access"}), 403

    # Get data from the request
    data = request.get_json()
    if not data or 'influencer_username' not in data:
        return jsonify({"error": "Influencer username is required"}), 400

    influencer_username = data['influencer_username']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    cur = conn.cursor()

    try:
        # Query to find influencer details
        cur.execute('''
            SELECT username, name, niche, category, reach, platform_presence
            FROM influencer_users
            WHERE username = ?
        ''', (influencer_username,))
        influencer_info = cur.fetchone()

        # Check if influencer exists
        if influencer_info:
            influencer = {
                'username': influencer_info["username"],
                'name': influencer_info["name"],
                'niche': influencer_info["niche"],
                'category': influencer_info["category"],
                'reach': influencer_info["reach"],
                'platform_presence': influencer_info["platform_presence"]
            }
            return jsonify({"influencer": influencer}), 200
        else:
            return jsonify({"message": "Influencer not found"}), 404

    except sqlite3.IntegrityError as e:
        return jsonify({"error": "Failed to retrieve influencer information", "details": str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cur.close()
        conn.close()


@app.route('/fetch_events', methods=['GET'])
def fetch_events():
    username = session.get('user')  # Assuming the username is stored in the session

    try:
        # Directly establishing connection to SQLite database
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # To access columns by name
        cursor = conn.cursor()

        # Query to fetch events where the logged-in influencer is involved
        query = """
            SELECT campaign_name, sponsor_username
            FROM events
            WHERE influencer_username = ?
        """
        cursor.execute(query, (username,))
        events = cursor.fetchall()
        conn.close()

        if events:
            # Convert each row to a dictionary
            events_list = [{'campaign_name': event['campaign_name'], 'sponsor_username': event['sponsor_username']} for event in events]
            return jsonify(events_list)
        else:
            return jsonify([])  # No events found

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_events1', methods=['GET'])
def fetch_events1():
    sponsor_username = session.get('user')

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    cursor = conn.cursor()

    cursor.execute("""
        SELECT campaign_name, influencer_username
        FROM events
        WHERE sponsor_username = ?
    """, (sponsor_username,))
    events = cursor.fetchall()

    if events:
        event_list = [{"campaign_name": event[0], "influencer_username": event[1]} for event in events]
        return jsonify(event_list)
    else:
        return jsonify({"error": "No events found for this sponsor."})
      
if __name__ == '__main__':
    try:
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS influencer_users(
                    username TEXT NOT NULL UNIQUE PRIMARY KEY,
                    password TEXT NOT NULL,
                    name TEXT,
                    niche TEXT,
                    category TEXT,
                    reach INTEGER,
                    phonenumber INTEGER,
                    platform_presence TEXT
                )
            """)
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS influencer_users1(
                    username TEXT NOT NULL UNIQUE PRIMARY KEY,
                    password TEXT NOT NULL,
                    name TEXT,
                    niche TEXT,
                    category TEXT,
                    reach INTEGER,
                    phonenumber INTEGER,
                    platform_presence TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                username TEXT NOT NULL UNIQUE PRIMARY KEY,
                password TEXT NOT NULL,
                role INTEGER NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admin(
                username TEXT NOT NULL UNIQUE PRIMARY KEY,
                password TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sponsor_users (
                username TEXT NOT NULL UNIQUE PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT,
                industry TEXT,
                budget REAL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                name TEXT NOT NULL UNIQUE PRIMARY KEY,
                description TEXT,
                start_date DATE,
                end_date DATE,
                budget REAL,
                visibility TEXT CHECK(visibility IN ('public', 'private')),
                goals TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ad_requests (
                campaign_name TEXT PRIMARY KEY,
                influencer_username TEXT,
                sponsor_username TEXT,
                messages TEXT,
                requirements TEXT,
                payment_amount REAL,
                status TEXT CHECK(status IN ('pending', 'accepted', 'rejected')),
                FOREIGN KEY (campaign_name) REFERENCES campaigns(name),
                FOREIGN KEY (influencer_username) REFERENCES influencer_users1(username)
                )
            """)
            cur.execute("""CREATE TABLE IF NOT EXISTS flagged_users_campaigns (
                name TEXT NOT NULL PRIMARY KEY,
                type TEXT NOT NULL,
                flag_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS ad_requests1 (
                campaign_name TEXT PRIMARY KEY,
                sponsor_username TEXT,
                influencer_username TEXT,
                messages TEXT,
                requirements TEXT,
                payment_amount REAL,
                status TEXT CHECK(status IN ('pending', 'accepted', 'rejected')),
                FOREIGN KEY (campaign_name) REFERENCES campaigns(name),
                FOREIGN KEY (influencer_username) REFERENCES influencer_users1(username)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS events(
                campaign_name TEXT ,
                influencer_username TEXT,
                sponsor_username TEXT,
                PRIMARY KEY (campaign_name, influencer_username, sponsor_username)
                )
            """)
            try:
                cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('prasadrao', 'lbnm12345'))
                cur.execute("INSERT INTO users (username, password,role) VALUES (?, ?,?)", ('prasadrao', 'lbnm12345',1))
            except sqlite3.IntegrityError:
                print("Admin user already exists.")            
            print("Tables created successfully !")
            conn.commit()
    except Exception as e:
        print("Error in table creation or connecting to server: ",e)
    app.run(debug=True)