from collections import defaultdict
import json

class ReferralTree:
    def __init__(self):
        self.tree = defaultdict(list)

    def add_referral(self, referrer, referred):
        self.tree[referrer].append(referred)

    def get_total_referrals(self, customer):
        def count_referrals(node):
            return 1 + sum(count_referrals(child) for child in self.tree[node])
        return count_referrals(customer) - 1  # Subtract 1 to exclude the customer itself

# Example Input
def handle_referral_tree(request_json):
    data = json.loads(request_json)
    action = data.get("action")
    tree = ReferralTree()
    
    for referral in data.get("referrals", []):
        tree.add_referral(referral["referrer"], referral["referred"])

    if action == "get_total_referrals":
        customer = data["customer"]
        result = tree.get_total_referrals(customer)
        return json.dumps({"customer": customer, "total_referrals": result})

# Example Usage
request_json = json.dumps({
    "action": "get_total_referrals",
    "referrals": [
        {"referrer": "Alice", "referred": "Bob"},
        {"referrer": "Alice", "referred": "Charlie"},
        {"referrer": "Bob", "referred": "David"}
    ],
    "customer": "Alice"
})
print(handle_referral_tree(request_json))
