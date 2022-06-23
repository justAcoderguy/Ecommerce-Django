from statistics import mode
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):
    """
    Inverntory Category Table ( using MPTT )
    MPTT is used for hierarchical models
    """
    name = models.CharField(
        max_length=100, 
        null=False, 
        unique=True, 
        blank=False, 
        verbose_name=_("category name"),
        help_text=_("format: required, max-100"),
        )
    slug = models.SlugField(
        max_length=150, 
        null=False, 
        unique=True,
        blank=False,
        verbose_name=_("url safe category name"),
        help_text=_("format: required, Please use letters, numbers, \
        underscore or hyphens"),
    )
    is_active = models.BooleanField(
        default=True,

    )

    # MPTT - https://django-mptt.readthedocs.io/en/latest/overview.html
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Parent of Category"),
        related_name="children",
        help_text=_("Format: not requred"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")


class Product(models.Model):
    """
        Product details table
    """
    
    web_id = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("product website ID"),
        help_text=_("format: required, unique"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("product safe URL"),
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens"
        ),
    )
    name = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("product name"),
        help_text=_("format: required, max-255"),
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("product description"),
        help_text=_("format: required"),
    )
    # Question : Is this 'TreeManyToManyField' implemented inside as reqd???
    category = TreeManyToManyField(Category)
    is_active = models.BooleanField(
        unique=False,
        null=False,
        blank=False,
        default=True,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date product created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        # Any field with the auto_now attribute set will also 
        # inherit editable=False and therefore will not show up in 
        # the admin panel.
        auto_now=True,
        verbose_name=_("date product last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return self.name
    