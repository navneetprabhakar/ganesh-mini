import copy
import unittest
import tempfile
import shlex
from pathlib import Path
from unittest.mock import patch
from scripts.train import gcloud_gate3_qualification as qualification
from scripts.train.gcloud_gate3_qualification import boundary, seal, PROJECT, ZONE


class QualificationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.card = {'schema_version':'ganesh-mini-gate3-qualification-gcloud/v1',
                     'absolute_incremental_ceiling_usd':'5','quality_pilot_allowed':False,
                     'maximum_vm_seconds':7200,'probe_rows':16,'project':PROJECT,'zone':ZONE}
        self.card['execution_sha256']=seal(self.card)

    def test_exact_qualification_boundary(self):
        boundary(self.card)

    def test_tampering_is_rejected(self):
        card=copy.deepcopy(self.card); card['probe_rows']=17
        with self.assertRaises(ValueError): boundary(card)

    def test_resealed_expansion_is_rejected(self):
        for key,value in [('quality_pilot_allowed',True),('maximum_vm_seconds',7201),
                          ('absolute_incremental_ceiling_usd','6'),('project','other')]:
            card=copy.deepcopy(self.card); card.pop('execution_sha256'); card[key]=value
            card['execution_sha256']=seal(card)
            with self.assertRaises(ValueError): boundary(card)

    def test_zone_alternative_stays_same_region(self):
        for zone in ('us-east1-b','us-east1-d'):
            card=copy.deepcopy(self.card); card.pop('execution_sha256'); card['zone']=zone
            card['execution_sha256']=seal(card); boundary(card)
        card.pop('execution_sha256'); card['zone']='asia-south1-a'; card['execution_sha256']=seal(card)
        with self.assertRaises(ValueError): boundary(card)

    def test_central_fallback_requires_transfer_reserve(self):
        card=copy.deepcopy(self.card); card.pop('execution_sha256'); card['zone']='us-central1-a'
        card['execution_sha256']=seal(card)
        with self.assertRaises(ValueError): boundary(card)
        card.pop('execution_sha256'); card['cross_region_transfer_reserve_usd']='0.50'
        card['execution_sha256']=seal(card); boundary(card)

    def test_watcher_finalizes_only_stopped_vm(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder); card=copy.deepcopy(self.card); card.pop('execution_sha256')
            card['instance']='exact-approved-vm'; card['execution_sha256']=seal(card)
            qualification.save(out/'execution-card.json',card)
            with patch.object(qualification,'inspect',return_value={'status':'TERMINATED'}) as observed, \
                 patch.object(qualification,'finalize') as finalized:
                qualification.watch(out)
                observed.assert_called_once_with(out); finalized.assert_called_once_with(out)

    def test_duplicate_watcher_cannot_inspect_or_mutate(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder); card=copy.deepcopy(self.card); card.pop('execution_sha256')
            card['instance']='exact-approved-vm'; card['execution_sha256']=seal(card)
            qualification.save(out/'execution-card.json',card)
            qualification.save(out/'watcher-started.json',{'pid':123})
            with patch.object(qualification,'inspect') as observed:
                with self.assertRaises(FileExistsError): qualification.watch(out)
                observed.assert_not_called()

    def test_startup_overrides_old_image_entrypoint(self):
        script=(qualification.ROOT/'scripts/train/gcloud_gate3_qualification_startup.sh').read_text()
        command=script.split('docker run ',1)[1].replace('\\\n',' ')
        args=shlex.split(command)
        self.assertEqual(args[args.index('--entrypoint')+1],'python3')
        self.assertEqual(args[args.index('$image')+1:args.index('$image')+3],
                         ['-B','scripts/train/measure_gate3_capability_throughput.py'])

    def test_resealed_prior_spending_expansion_is_rejected(self):
        for spending in ('1.01','2','-1'):
            card=copy.deepcopy(self.card); card.pop('execution_sha256')
            card['prior_spend_reserve_usd']=spending; card['execution_sha256']=seal(card)
            with self.assertRaises(ValueError): boundary(card)

    def canonical_card(self):
        card=copy.deepcopy(self.card); card.pop('execution_sha256')
        card.update(prior_spend_reserve_usd='2.00',
                    canonical_rescue_plan_sha256=qualification.CANONICAL_RESCUE_PLAN,
                    maximum_additional_allocated_starts=1,
                    prior_paid_attempts=['20260929T112530Z','20260929T114450Z'],
                    support_reserve_usd='0.737956976',cross_region_transfer_reserve_usd='0.50',
                    provider_two_hour_upper_usd='1.762043024',
                    inputs={'model_materializer':{'sha256':qualification.MATERIALIZER_SHA}})
        card['execution_sha256']=seal(card)
        return card

    def test_canonical_rescue_exact_cumulative_budget(self):
        boundary(self.canonical_card())

    def test_canonical_rescue_cannot_reset_cost_or_expand_scope(self):
        for key,value in [('canonical_rescue_plan_sha256','0'*64),('maximum_additional_allocated_starts',2),
                          ('prior_paid_attempts',[]),('support_reserve_usd','1'),
                          ('cross_region_transfer_reserve_usd','0')]:
            card=self.canonical_card();card.pop('execution_sha256');card[key]=value;card['execution_sha256']=seal(card)
            with self.assertRaises(ValueError): boundary(card)

    def test_canonical_rescue_requires_exact_user_approved_plan(self):
        with self.assertRaises(ValueError): qualification.canonical_retry_reserve(Path('anything'),'0'*64)

    def test_canonical_materializer_precedes_probe(self):
        script=(qualification.ROOT/'scripts/train/gcloud_gate3_qualification_startup.sh').read_text()
        self.assertIn('env PYTHONPATH="$work/workspace" python3 -B "$work/model_materializer"',script)
        self.assertIn('--materialize-dir "$work/model"',script)
        self.assertLess(script.index('--materialize-dir'),script.index('docker run '))

    def test_approved_l4_retry_carries_three_prior_starts_within_same_ceiling(self):
        card=copy.deepcopy(self.card);card.pop('execution_sha256')
        card.update(prior_spend_reserve_usd='2.50',usable_floor_plan_sha256=qualification.USABLE_FLOOR_PLAN,
            gpu_hardware_contract='ganesh-mini-gate3-l4-usable-v1',
            l4_usable_floor_bytes=23622320128,other_gpu_floor_bytes=24000000000,
            maximum_additional_allocated_starts=1,
            prior_paid_attempts=['20260929T112530Z','20260929T114450Z','20260929T133600Z'],
            support_reserve_usd='0.237956976',cross_region_transfer_reserve_usd='0.50',
            provider_two_hour_upper_usd='1.762043024',
            inputs={'workspace_archive':{'sha256':qualification.WORKSPACE_V4_SHA},
                    'model_materializer':{'sha256':qualification.MATERIALIZER_SHA}})
        card['execution_sha256']=seal(card)
        boundary(card)
        for key,value in [('prior_spend_reserve_usd','2.00'),('support_reserve_usd','0.737956976'),
                          ('maximum_additional_allocated_starts',2),('usable_floor_plan_sha256','0'*64),
                          ('l4_usable_floor_bytes',24000000000)]:
            changed=copy.deepcopy(card);changed.pop('execution_sha256');changed[key]=value
            changed['execution_sha256']=seal(changed)
            with self.assertRaises(ValueError): boundary(changed)

    def test_approved_l4_retry_requires_exact_unchanged_plan(self):
        with self.assertRaises(ValueError):
            qualification.usable_floor_retry_reserve(Path('anything'),'0'*64)

    def test_stopped_vm_does_not_require_serial_endpoint(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder); card=copy.deepcopy(self.card); card.pop('execution_sha256')
            card['instance']='exact-approved-vm'; card['execution_sha256']=seal(card)
            qualification.save(out/'execution-card.json',card)
            value={'status':'TERMINATED','name':'exact-approved-vm'}
            with patch.object(qualification,'run',return_value=value) as command:
                self.assertEqual(qualification.inspect(out),value)
                self.assertEqual(command.call_count,1)

    def test_serial_failure_cannot_hide_authoritative_vm_state(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder); card=copy.deepcopy(self.card); card.pop('execution_sha256')
            card['instance']='exact-approved-vm'; card['execution_sha256']=seal(card)
            qualification.save(out/'execution-card.json',card)
            value={'status':'RUNNING','name':'exact-approved-vm'}
            with patch.object(qualification,'run',side_effect=[value,RuntimeError('serial not ready')]):
                self.assertEqual(qualification.inspect(out),value)

if __name__=='__main__': unittest.main()
