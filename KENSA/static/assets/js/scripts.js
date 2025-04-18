function populateEditForm(id, name, email, phone, item_name, amount, customer_comments, status, ai_analysis) {
    document.getElementById('editCustomerId').value = id;
    document.getElementById('editCustomerName').value = name;
    document.getElementById('editCustomerEmail').value = email;
    document.getElementById('editCustomerPhone').value = phone;
    document.getElementById('editCustomerItemName').value = item_name;
    document.getElementById('editCustomerAmount').value = amount;
    document.getElementById('editCustomerComments').value = customer_comments;
    document.getElementById('editCustomerStatus').value = status;
    // If you have ai_analysis field
    // document.getElementById('editCustomerAiAnalysis').value = ai_analysis;
}

  function populateDeleteForm(id) {
    document.getElementById('deleteCustomerId').value = id;
  }
