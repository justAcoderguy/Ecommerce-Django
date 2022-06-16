from statistics import mode
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category():
    """
    Inverntory Category Table.
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

