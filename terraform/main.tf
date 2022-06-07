/* it would be really cool if this worked out of the box, for helm though kubectl 
 needs the cluster context to be set and I can't think of a way to do that hassleless
resource "linode_nodebalancer" "smplverse-lb" {
  region = var.region
  label = var.lb-label
}

module "nginx-controller" {
  source = "terraform-iaac/nginx-controller/helm"
  ip_address = linode_nodebalancer.smplverse-lb.ipv4

  depends_on = [
    linode_nodebalancer.smplverse-lb,
    linode_lke_cluster.smplverse
  ]
}
*/

resource "linode_lke_cluster" "smplverse" {
    k8s_version = var.k8s_version
    label = var.label
    region = var.region

    dynamic "pool" {
        for_each = var.pools
        content {
            type  = pool.value["type"]
            count = pool.value["count"]
        }
    }
}

output "kubeconfig" {
   value = linode_lke_cluster.smplverse.kubeconfig
   sensitive = true
}

output "api_endpoints" {
   value = linode_lke_cluster.smplverse.api_endpoints
}

output "status" {
   value = linode_lke_cluster.smplverse.status
}

output "id" {
   value = linode_lke_cluster.smplverse.id
}

output "pool" {
   value = linode_lke_cluster.smplverse.pool
}
