from django.db import models
from django.conf import settings


class SteelSheet(models.Model):
    lot_number = models.CharField(max_length=100)        # SKU or Lot Number
    part_name = models.CharField(max_length=200)
    thickness = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # Add any fields you want to filter/search here
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lot_number} - {self.part_name}"



class SteelSheetInspection(models.Model):
    sheet = models.ForeignKey(SteelSheet, on_delete=models.CASCADE, related_name='inspections')
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    inspection_date = models.DateField(auto_now_add=True)

    # Inspection checkpoints
    surface_deformation = models.BooleanField(default=False, help_text="Surface deformation detected?")
    scratches_percent = models.PositiveSmallIntegerField(default=0, help_text="Percent of scratches on surface")
    dent = models.BooleanField(default=False)
    stain = models.BooleanField(default=False)
    other_remarks = models.CharField(max_length=255, blank=True, null=True)
    conductivity_test = models.CharField(max_length=8, choices=[('pass', 'Pass'), ('fail', 'Fail')], default='pass')
    decision = models.CharField(
        max_length=12,
        choices=[('approve', 'Approve'), ('disapprove', 'Disapprove')],
        default='approve'
    )
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection for {self.sheet} on {self.inspection_date}"
    


class ScanLog(models.Model):
    product_id = models.CharField(max_length=100)
    machine_id = models.CharField(max_length=100)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="scanlogs"
    )
    date_scanned = models.DateField()
    time_scanned = models.TimeField()
    condition = models.CharField(max_length=100)  # e.g. 'OK', 'Defective', etc.
    num_defects = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='scan_images/', null=True, blank=True)
    qc_manager_tagged = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="qc_tagged_scans"
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_id} - {self.machine_id} @ {self.date_scanned} {self.time_scanned}"
