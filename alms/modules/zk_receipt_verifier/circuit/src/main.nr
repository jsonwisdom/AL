fn main(
    nullifier_hash: Field,
    promotion_id: Field,
    authorized_primitive: Field,
    provided_primitive: Field,
    valid_from: Field,
    valid_until: Field,
    current_time: Field,
) {
    // Primitive authorization check
    assert(authorized_primitive == provided_primitive);

    // Time window check
    assert(current_time >= valid_from);
    assert(current_time <= valid_until);

    // Nullifier must not be zero
    assert(nullifier_hash != 0);

    // Promotion id must not be zero
    assert(promotion_id != 0);
}
