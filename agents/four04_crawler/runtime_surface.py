from agents.four04_crawler.proof_blob_surface import AllowedSurface

# 404 agent runtime constitution
# Strict subset of full AllowedSurface membrane.
RUNTIME_ALLOWED_404 = {
    AllowedSurface.FOUND,
    AllowedSurface.NOT_FOUND,
    AllowedSurface.VERSION_DRIFT,
    AllowedSurface.CRAWLER_BLOCKED,
}
