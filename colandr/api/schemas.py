from marshmallow import Schema, fields, pre_load
from marshmallow.validate import Email, Length, OneOf, Range
from webargs import missing

from ..lib import constants
from ..lib.sanitizers import CITATION_FIELD_SANITIZERS, sanitize_type


class UserSchema(Schema):
    id = fields.Int(
        dump_only=True, validate=Range(min=1, max=constants.MAX_INT))
    created_at = fields.DateTime(
        dump_only=True, format='iso')
    name = fields.Str(
        required=True, validate=Length(min=1, max=200))
    email = fields.Email(
        required=True, validate=[Email(), Length(max=200)])
    password = fields.Str(
        load_only=True, required=True, validate=Length(min=6, max=60))

    class Meta:
        strict = True


class ReviewSchema(Schema):
    id = fields.Int(
        dump_only=True, validate=Range(min=1, max=constants.MAX_INT))
    created_at = fields.DateTime(
        dump_only=True, format='iso')
    owner_user_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_INT))
    name = fields.Str(
        required=True, validate=Length(max=500))
    description = fields.Str(
        missing=None)
    status = fields.Str(
        validate=OneOf(['active', 'archived']))
    num_citation_screening_reviewers = fields.Int(
        validate=Range(min=1, max=2))
    num_fulltext_screening_reviewers = fields.Int(
        validate=Range(min=1, max=2))

    class Meta:
        strict = True


class ReviewPlanPICO(Schema):
    population = fields.Str(
        validate=Length(max=300))
    intervention = fields.Str(
        validate=Length(max=300))
    comparison = fields.Str(
        validate=Length(max=300))
    outcome = fields.Str(
        validate=Length(max=300))

    class Meta:
        strict = True


class ReviewPlanKeyterm(Schema):
    group = fields.Str(
        required=True, validate=Length(max=100))
    term = fields.Str(
        required=True, validate=Length(max=100))
    synonyms = fields.List(
        fields.Str(validate=Length(max=100)),
        missing=[])

    class Meta:
        strict = True


class ReviewPlanSelectionCriterion(Schema):
    label = fields.Str(
        required=True, validate=Length(max=25))
    description = fields.Str(
        validate=Length(max=300))

    class Meta:
        strict = True


class ReviewPlanDataExtractionItem(Schema):
    label = fields.Str(
        required=True, validate=Length(max=25))
    description = fields.Str(
        validate=Length(max=300))
    field_type = fields.Str(
        required=True,
        validate=OneOf(['bool', 'date', 'int', 'float', 'str',
                        'select_one', 'select_many',
                        'country']))
    allowed_values = fields.List(
        fields.Str())

    class Meta:
        strict = True


class ReviewPlanSuggestedKeyterms(Schema):
    sample_size = fields.Int(
        required=True, validate=Range(min=1))
    incl_keyterms = fields.List(
        fields.Str(), required=True)
    excl_keyterms = fields.List(
        fields.Str(), required=True)

    class Meta:
        strict = True


class ReviewPlanSchema(Schema):
    id = fields.Int(
        dump_only=True)
    review_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_INT))
    objective = fields.Str()
    research_question = fields.List(
        fields.Str(validate=Length(max=300)))
    pico = fields.Nested(
        ReviewPlanPICO)
    keyterms = fields.Nested(
        ReviewPlanKeyterm, many=True)
    selection_criteria = fields.Nested(
        ReviewPlanSelectionCriterion, many=True)
    data_extraction_form = fields.Nested(
        ReviewPlanDataExtractionItem, many=True)
    boolean_search_query = fields.Str()
    suggested_keyterms = fields.Nested(
        ReviewPlanSuggestedKeyterms)

    class Meta:
        strict = True


class Deduplication(Schema):
    is_duplicate = fields.Bool(
        required=True)
    canonical_id = fields.Int(
        validate=Range(min=1, max=constants.MAX_BIGINT))
    duplicate_score = fields.Float(
        validate=Range(min=0.0, max=1.0))
    user_id = fields.Int(
        missing=None, validate=Range(min=1, max=constants.MAX_INT))

    class Meta:
        strict = True


class ScreeningSchema(Schema):
    id = fields.Int(
        dump_only=True)
    created_at = fields.DateTime(
        dump_only=True, format='iso')
    review_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_INT))
    user_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_INT))
    citation_id = fields.Int(
        missing=None, validate=Range(min=1, max=constants.MAX_BIGINT))
    fulltext_id = fields.Int(
        missing=None, validate=Range(min=1, max=constants.MAX_BIGINT))
    status = fields.Str(
        validate=OneOf(['included', 'excluded']))
    exclude_reasons = fields.List(
        fields.Str(validate=Length(max=25)), missing=None)

    class Meta:
        strict = True


class CitationSchema(Schema):
    id = fields.Int(
        dump_only=True)
    created_at = fields.DateTime(
        dump_only=True, format='iso')
    review_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_INT))
    status = fields.Str(
        validate=OneOf(['not_screened', 'screened_once', 'screened_twice',
                        'conflict', 'excluded', 'included']))
    deduplication = fields.Nested(
        Deduplication)
    tags = fields.List(
        fields.Str(validate=Length(max=25)))
    type_of_work = fields.Str(
        validate=Length(max=25))
    title = fields.Str(
        validate=Length(max=250))
    secondary_title = fields.Str(
        validate=Length(max=250))
    abstract = fields.Str()
    pub_year = fields.Int(
        validate=Range(min=1, max=constants.MAX_SMALLINT))
    pub_month = fields.Int(
        validate=Range(min=1, max=constants.MAX_SMALLINT))
    authors = fields.List(
        fields.Str(validate=Length(max=100)))
    keywords = fields.List(
        fields.Str(validate=Length(max=100)))
    type_of_reference = fields.Str(
        validate=Length(max=50))
    journal_name = fields.Str(
        validate=Length(max=100))
    volume = fields.Str(
        validate=Length(max=20))
    issue_number = fields.Str(
        validate=Length(max=20))
    doi = fields.Str(
        validate=Length(max=100))
    issn = fields.Str(
        validate=Length(max=20))
    publisher = fields.Str(
        validate=Length(max=100))
    language = fields.Str(
        validate=Length(max=50))
    other_fields = fields.Dict()
    screenings = fields.Nested(
        ScreeningSchema, many=True)

    @pre_load(pass_many=False)
    def sanitize_citation_record(self, record):
        sanitized_record = {'other_fields': {}}
        for key, value in record.items():
            if value is missing or key == 'screenings':
                continue
            try:
                sanitized_record[key] = CITATION_FIELD_SANITIZERS[key](value)
            except KeyError:
                sanitized_record['other_fields'][key] = sanitize_type(value, str)
        return sanitized_record

    class Meta:
        strict = True


class FulltextExtractedDataItem(Schema):
    label = fields.Str(
        required=True, validate=Length(max=25))
    # validation handled in API Resource
    # based on values in ReviewPlanDataExtractionItem
    value = fields.Raw(
        required=True)

    class Meta:
        strict = True


class FulltextExtractedDataSchema(Schema):
    id = fields.Int(
        dump_only=True)
    created_at = fields.DateTime(
        dump_only=True, format='iso')
    review_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_INT))
    fulltext_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_BIGINT))
    extracted_data = fields.Nested(
        FulltextExtractedDataItem, many=True)

    class Meta:
        strict = True


class FulltextSchema(Schema):
    id = fields.Int(
        dump_only=True)
    created_at = fields.DateTime(
        dump_only=True, format='iso')
    citation_id = fields.Int(
        required=True, validate=Range(min=1, max=constants.MAX_BIGINT))
    status = fields.Str(
        validate=OneOf(['not_screened', 'screened_once', 'screened_twice',
                        'included', 'excluded', 'conflict']))
    filename = fields.Str(
        required=True)
    screenings = fields.Nested(
        ScreeningSchema, many=True)
    extracted_data = fields.Nested(
        FulltextExtractedDataSchema)
    citation = fields.Nested(
        CitationSchema)

    class Meta:
        strict = True
